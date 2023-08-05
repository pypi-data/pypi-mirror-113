from . import functional


class Compose:
    """Composes several transforms together.

    Parameters:
        transforms (list of ``Transform`` objects): list of transform(s) to compose. Even when using a single transform, the Compose wrapper is necessary.

    Example:
        >>> transforms.Compose([
        >>>     transforms.Denoise(),
        >>>     transforms.ToTensor(),
        >>> ])
    """

    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        for t in self.transforms:
            events, images = t(
                events=events,
                images=images,
                sensor_size=sensor_size,
                ordering=ordering,
                multi_image=multi_image,
            )
        if multi_image and images.all() != None:
            return events, images
        else:
            return events

    def __repr__(self):
        format_string = self.__class__.__name__ + "("
        for t in self.transforms:
            format_string += "\n"
            format_string += "    {0}".format(t)
        format_string += "\n)"
        return format_string


class Crop:
    """Crops the sensor size to a smaller sensor.
    Removes events outsize of the target sensor and maps.

    x' = x - new_sensor_start_x

    y' = y - new_sensor_start_y

    Parameters:
        target_size: size of the sensor that was used [W',H']
    """
    
    def __init__(self, target_size):
        self.target_size = target_size

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        return functional.crop_numpy(
            events=events,
            sensor_size=sensor_size,
            ordering=ordering,
            images=images,
            multi_image=multi_image,
            target_size=self.target_size,
        )


class Denoise:
    """Drops events that are 'not sufficiently connected to other events in the recording.'
    In practise that means that an event is dropped if no other event occured within a spatial neighbourhood
    of 1 pixel and a temporal neighbourhood of filter_time time units. Useful to filter noisy recordings
    where events occur isolated in time.

    Parameters:
        filter_time: maximum temporal distance to next event, otherwise dropped.
                    Lower values will mean higher constraints, therefore less events.
    """
    def __init__(self, filter_time=10000):
        self.filter_time = filter_time

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = functional.denoise_numpy(
            events=events,
            sensor_size=sensor_size,
            ordering=ordering,
            filter_time=self.filter_time,
        )
        return events, images


class DropEvents:
    """Randomly drops events with drop_probability.

    Parameters:
        drop_probability: probability of dropping out event.
        random_drop_probability: randomize the dropout probability
                                 between 0 and drop_probability.
    """    
    def __init__(self, drop_probability=0.5, random_drop_probability=False):
        self.drop_probability = drop_probability
        self.random_drop_probability = random_drop_probability

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = functional.drop_events_numpy(
            events, self.drop_probability, self.random_drop_probability
        )
        return events, images


class FlipLR:
    """Flips events and images in x. Pixels map as:

        x' = width - x

    Parameters:
        flip_probability: probability of performing the flip
    """
    def __init__(self, flip_probability=0.5):
        self.flip_probability_lr = flip_probability

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        return functional.flip_lr_numpy(
            events=events,
            sensor_size=sensor_size,
            ordering=ordering,
            images=images,
            multi_image=multi_image,
            flip_probability=self.flip_probability_lr,
        )


class FlipPolarity:
    """Flips polarity of individual events with flip_probability.
    Changes polarities 1 to -1 and polarities [-1, 0] to 1

    Parameters:
        flip_probability: probability of flipping individual event polarities
    """
    def __init__(self, flip_probability=0.5):
        self.flip_probability_pol = flip_probability

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = functional.flip_polarity_numpy(
            events=events, ordering=ordering, flip_probability=self.flip_probability_pol
        )
        return events, images


class FlipUD:
    """
    Flips events and images in y. Pixels map as:

        y' = height - y

    Parameters:
        flip_probability: probability of performing the flip
    """
    def __init__(self, flip_probability=0.5):
        self.flip_probability_ud = flip_probability

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        return functional.flip_ud_numpy(
            events=events,
            sensor_size=sensor_size,
            ordering=ordering,
            images=images,
            multi_image=multi_image,
            flip_probability=self.flip_probability_ud,
        )


class MaskHotPixel:
    """Drops events for certain pixel locations, to suppress pixels that constantly fire (e.g. due to faulty hardware).

    Parameters:
        coordinates: list of (x,y) coordinates for which all events will be deleted.
    """
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = functional.mask_hot_pixel(
            events=events,
            sensor_size=sensor_size,
            ordering=ordering,
            coordinates=self.coordinates,
        )
        return events, images


class RefractoryPeriod:
    """Sets a refractory period for each pixel, during which events will be
    ignored/discarded. We keep events if:

        .. math::
            t_n - t_{n-1} > t_{refrac}

    Parameters:
        refractory_period: refractory period for each pixel in seconds
    """

    def __init__(self, refractory_period=0.5):
        self.refractory_period = refractory_period

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = functional.refractory_period_numpy(
            events, sensor_size, ordering, self.refractory_period
        )
        return events, images


class SpatialJitter:
    """Changes position for each pixel by drawing samples from a multivariate
    Gaussian distribution with the following properties:

        mean = [x,y]
        covariance matrix = [[variance_x, sigma_x_y],[sigma_x_y, variance_y]]

    Jittered events that lie outside the focal plane will be dropped if clip_outliers is True.

    Parameters:
        variance_x: squared sigma value for the distribution in the x direction
        variance_y: squared sigma value for the distribution in the y direction
        sigma_x_y: changes skewness of distribution, only change if you want shifts along diagonal axis.
        integer_coordinates: when True, shifted x and y values will be integer coordinates
        clip_outliers: when True, events that have been jittered outside the focal plane will be dropped.
    """
    def __init__(
        self,
        variance_x=1,
        variance_y=1,
        sigma_x_y=0,
        integer_coordinates=True,
        clip_outliers=True,
    ):
        self.variance_x = variance_x
        self.variance_y = variance_y
        self.sigma_x_y = sigma_x_y
        self.integer_coordinates = integer_coordinates
        self.clip_outliers = clip_outliers

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = functional.spatial_jitter_numpy(
            events,
            sensor_size,
            ordering,
            self.variance_x,
            self.variance_y,
            self.sigma_x_y,
            self.integer_coordinates,
            self.clip_outliers,
        )
        return events, images


class SpatioTemporalTransform:
    """Transform all events spatial and temporal locations based on
    given spatial transform matrix and temporal transform vector.

    Parameters:
        spatial_transform: 3x3 matrix which can be used to perform rigid (translation and rotation),
                           non-rigid (scaling and shearing), and non-affine transformations. Generic to user input.
        temporal_transform: scale time between events and offset temporal location based on 2 member vector.
                            Used as arguments to time_skew method.
        roll: boolean input to determine if transformed events will be translated across sensor boundaries (True).
              Otherwise, events will be clipped at sensor boundaries.
    """
    def __init__(self, spatial_transform, temporal_transform, roll=False):
        self.spatial_transform = spatial_transform
        self.temporal_transform = temporal_transform
        self.roll = roll

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = functional.st_transform(
            events,
            sensor_size,
            ordering,
            self.spatial_transform,
            self.temporal_transform,
            self.roll,
        )
        return events, images


class TimeJitter:
    """Changes timestamp for each event by drawing samples from a
    Gaussian distribution with the following properties:

        mean = [t]
        std = std

    Will clip negative timestamps by default.

    Parameters:
        std: change the standard deviation of the time jitter
        integer_jitter: will round the jitter that is added to timestamps
        clip_negative: drops events that have negative timestamps
        sort_timestamps: sort the events by timestamps
    """
    def __init__(
        self, std=1, integer_jitter=False, clip_negative=False, sort_timestamps=False
    ):
        self.std = std
        self.integer_jitter = integer_jitter
        self.clip_negative = clip_negative
        self.sort_timestamps = sort_timestamps

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = functional.time_jitter_numpy(
            events,
            ordering,
            self.std,
            self.integer_jitter,
            self.clip_negative,
            self.sort_timestamps,
        )
        return events, images


class TimeReversal:
    """Temporal flip is defined as:

        .. math::
           t_i' = max(t) - t_i

           p_i' = -1 * p_i

    Parameters:
        flip_probability: probability of performing the flip
    """
    def __init__(self, flip_probability=0.5):
        self.flip_probability_t = flip_probability

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        return functional.time_reversal_numpy(
            events=events,
            sensor_size=sensor_size,
            ordering=ordering,
            images=images,
            multi_image=multi_image,
            flip_probability=self.flip_probability_t,
        )


class TimeSkew:
    """Skew all event timestamps according to a linear transform,
    potentially sampled from a distribution of acceptable functions.

    Parameters:
        coefficient: a real-valued multiplier applied to the timestamps of the events.
                     E.g. a coefficient of 2.0 will double the effective delay between any
                     pair of events.
        offset: value by which the timestamps will be shifted after multiplication by
                the coefficient. Negative offsets are permissible but may result in
                in an exception if timestamps are shifted below 0.
    """
    def __init__(self, coefficient=0.9, offset=0):
        self.coefficient = coefficient
        self.offset = offset

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = functional.time_skew_numpy(
            events, ordering, self.coefficient, self.offset
        )
        return events, images


class UniformNoise:
    """
    Introduces a fixed number of noise depending on sensor size and noise
    density factor, uniformly distributed across the focal plane and in time.

    Parameters:
        scaling_factor_to_micro_sec: this is a scaling factor to get to micro
                                     seconds from the time resolution used in the event stream,
                                     as the noise time resolution is fixed to 1 micro second.
        noise_density: A noise density of 1 will mean one noise event for every
                       pixel of the sensor size for every micro second.
    """
    def __init__(self, scaling_factor_to_micro_sec=1, noise_density=1e-8):
        self.scaling_factor_to_micro_sec = scaling_factor_to_micro_sec
        self.noise_density = noise_density

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        surfaces = functional.uniform_noise_numpy(
            events, sensor_size, ordering, self.scaling_factor_to_micro_sec, self.noise_density
        )
        return events, images


class ToAveragedTimesurface:
    """Representation that creates averaged timesurfaces for each event for one recording. Taken from the paper 
    Sironi et al. 2018, HATS: Histograms of averaged time surfaces for robust event-based object classification
    https://openaccess.thecvf.com/content_cvpr_2018/papers/Sironi_HATS_Histograms_of_CVPR_2018_paper.pdf

    Parameters:
        cell_size (int): size of each square in the grid
        surface_size (int): has to be odd
        time_window (float): how far back to look for past events for the time averaging
        tau (float): time constant to decay events around occuring event with.
        decay (str): can be either 'lin' or 'exp', corresponding to linear or exponential decay.
        merge_polarities (bool): flag that tells whether polarities should be taken into account separately or not.
    """
    def __init__(
        self,
        cell_size=10,
        surface_size=7,
        temporal_window=5e5,
        tau=5e3,
        decay="lin",
        merge_polarities=False,
    ):
        assert surface_size % 2 == 1
        self.cell_size = cell_size
        self.surface_size = surface_size
        self.temporal_window = temporal_window
        self.tau = tau
        self.decay = decay
        self.merge_polarities = merge_polarities

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        surfaces = functional.to_averaged_timesurface(
            events,
            sensor_size,
            ordering,
            self.cell_size,
            self.surface_size,
            self.temporal_window,
            self.tau,
            self.decay,
            self.merge_polarities,
        )
        return surfaces, images


class ToFrame:
    """Accumulate events to frames by slicing along constant time (time_window), 
    constant number of events (spike_count) or constant number of frames (time_bin_count / event_bin_count).

    Parameters:
        events: ndarray of shape [num_events, num_event_channels]
        sensor_size: size of the sensor that was used [W,H]
        ordering: ordering of the event tuple inside of events.
        time_window (None): time window length for one frame.
        spike_count (None): number of events per frame.
        time_bin_count (None): fixed number of frames, sliced along time axis.
        event_bin_count (None): fixed number of frames, sliced along number of events in the recording.
        overlap (0.): overlap between frames defined either in time in us, number of events or number of bins.
        include_incomplete (False): if True, includes overhang slice when time_window or spike_count is specified. Not valid for bin_count methods.
        merge_polarities (False): if True, merge polarity channels to a single channel.
    """
    def __init__(self, time_window=None, spike_count=None, time_bin_count=None, event_bin_count=None, overlap=0., include_incomplete=False, merge_polarities=False):
        self.time_window = time_window
        self.spike_count = spike_count
        self.time_bin_count = time_bin_count
        self.event_bin_count = event_bin_count
        self.overlap = overlap
        self.include_incomplete = include_incomplete
        self.merge_polarities = merge_polarities

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        frames = functional.to_frame_numpy(
            events=events,
            sensor_size=sensor_size,
            ordering=ordering,
            time_window=self.time_window,
            spike_count=self.spike_count,
            time_bin_count=self.time_bin_count,
            event_bin_count=self.event_bin_count,
            overlap=self.overlap,
            include_incomplete=self.include_incomplete,
            merge_polarities=self.merge_polarities,
        )
        return frames, images


class ToSparseTensor:
    """Turn event array (N,E) into sparse Tensor (B,T,W,H) if E is 4 (mostly event camera recordings),
    otherwise into sparse tensor (B,T,W) for mostly audio recordings."""

    def __init__(self, type='pytorch', merge_polarities=False):
        self.merge_polarities = merge_polarities
        self.type = type

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        if self.type == 'pytorch' or 'pt' or 'torch':
            tensor = functional.to_sparse_tensor_pytorch(
                events=events,
                sensor_size=sensor_size,
                ordering=ordering,
                merge_polarities=self.merge_polarities,
            )
        elif self.type == 'tensorflow' or 'tf':
            tensor = functional.to_sparse_tensor_tensorflow(
                events=events,
                sensor_size=sensor_size,
                ordering=ordering,
                merge_polarities=self.merge_polarities,
            )
        else:
            raise NotImplementedError
        return tensor, images


class ToTimesurface:
    """Representation that creates timesurfaces for each event in the recording. Modeled after the paper 
    Lagorce et al. 2016, Hots: a hierarchy of event-based time-surfaces for pattern recognition
    https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7508476

    Parameters:
        surface_dimensions (int, int): width does not have to be equal to height, however both numbers have to be odd.
        tau (float): time constant to decay events around occuring event with.
        decay (str): can be either 'lin' or 'exp', corresponding to linear or exponential decay.
        merge_polarities (bool): flag that tells whether polarities should be taken into account separately or not.
    """
    def __init__(
        self, surface_dimensions=(7, 7), tau=5e3, decay="lin", merge_polarities=False
    ):
        assert len(surface_dimensions) == 2
        assert surface_dimensions[0] % 2 == 1 and surface_dimensions[1] % 2 == 1
        self.surface_dimensions = surface_dimensions
        self.tau = tau
        self.decay = decay
        self.merge_polarities = merge_polarities

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        surfaces = functional.to_timesurface_numpy(
            events,
            sensor_size,
            ordering,
            self.surface_dimensions,
            self.tau,
            self.decay,
            self.merge_polarities,
        )
        return surfaces, images


class ToVoxelGrid(object):
    """Build a voxel grid with bilinear interpolation in the time domain from a set of events."""

    def __init__(self, num_time_bins=10):
        self.num_time_bins = num_time_bins

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        volume = functional.to_voxel_grid_numpy(
            events, sensor_size, ordering, self.num_time_bins
        )
        return volume, images


class Repeat:
    """Copies target n times. Useful to transform sample labels into sequences."""

    def __init__(self, repetitions):
        self.repetitions = repetitions

    def __call__(self, target):
        return np.tile(np.expand_dims(target, 0), [self.repetitions, 1])


class ToOneHotEncoding:
    """Transforms one or more targets into a one hot encoding scheme."""

    def __init__(self, n_classes):
        self.n_classes = n_classes

    def __call__(self, target):
        return np.eye(self.n_classes)[target]


class NumpyAsType:
    def __init__(self, cast_to):
        self.cast_to = cast_to

    def __call__(self, events, sensor_size, ordering, images=None, multi_image=None):
        events = events.astype(self.cast_to)

        if images is not None:
            images = images.astype(self.cast_to)

        return events, images
