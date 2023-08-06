"""CosmiX model to deposit charge by high energy ionising particles."""
from pathlib import Path
import numpy as np
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
except ImportError:
    # raise Warning('Matplotlib cannot be imported')
    plt = None
from cosmix.util import load_data_into_histogram, load_geant4_histogram


class Plotting:
    """Plotting class for CosmiX."""

    def __init__(self,
                 show_plots: bool = True,
                 output_dir: str = 'outputs',
                 geometry: dict = None
                 ) -> None:
        """TBW.

        :param show_plots:
        :param output_dir:
        """
        self.show_plots = show_plots
        self.output_dir = output_dir
        self.geometry = geometry

    def save_and_draw(self, fig_name: str):
        """TBW.

        :param fig_name:
        """
        plt.savefig(self.output_dir + '/' + fig_name + '.png')
        # plt.savefig(self.output_dir + '/' + fig_name + '.svg')
        if self.show_plots:
            plt.draw()

    def show(self):
        """TBW."""
        if self.show_plots:
            plt.show()

    # def plot_cdf(self, cdf, title: str = 'CDF', label=None, xlabel='', log=True):
    #     """TBW."""
    #     if isinstance(cdf, str) or isinstance(cdf, Path):
    #         cdf = np.load(cdf)
    #     plt.title(title)
    #     plt.xlabel(xlabel)
    #     if log:
    #         plt.semilogx(cdf[:, 0], cdf[:, 1], '.', label=label, markersize=2.)
    #     else:
    #         plt.plot(cdf[:, 0], cdf[:, 1], '.', label=label, markersize=2.)
    #     if label:
    #         plt.legend()
    #     self.save_and_draw('tars_plot_'+title.replace(' ', '_'))
    #
    # def plot_spectrum_cdf(self):
    #     """TBW."""
    #     plt.figure()
    #     plt.semilogx(self.tars.spectrum_cdf[:, 0], self.tars.spectrum_cdf[:, 1], '.')
    #     plt.title('Spectrum CDF')
    #     plt.xlabel('Energy (MeV)')
    #     self.save_and_draw('tars_plot_spectrum_cdf')
    #
    # def plot_spectrum_hist(self, data):
    #     """TBW."""
    #     plt.figure()
    #     plt.title('Proton flux spectrum sampled by TARS')
    #     plt.xlabel('Energy (MeV)')
    #     plt.ylabel('Counts')
    #     # plt.ylabel('Flux (1/(s*MeV))')
    #     # plt.loglog(lin_energy_range, flux_dist)
    #
    #     if isinstance(data, str):
    #         if data.endswith('.npy'):
    #             data = np.load(data)
    #
    #     hist_bins = 250
    #     # hist_range = (1e-1, 1e5)
    #     # col = (0, 1, 1, 1)
    #     plt.hist(data, bins=np.logspace(np.log10(0.1), np.log10(1e5), hist_bins))
    #     plt.gca().set_xscale("log")
    #     # plt.legend(loc='upper right')
    #     self.save_and_draw('tars_spectrum')

    # def plot_spectra(self, log=False):
    #     """TBW."""
    #     plt.figure()
    #     plt.title('Proton spectra')
    #     plt.xlabel('Energy (MeV)')
    #     plt.ylabel('Counts')
    #     hist_range = (1e-1, 1e5)
    #     hist_bins = 400
    #     hist_bins = np.logspace(np.log10(hist_range[0]), np.log10(hist_range[1]), hist_bins)
    #     # plt.axis([hist_range[0], hist_range[1], 1., 1.e+3])
    #     plt.ylim([0., 300])
    #
    #     hist_names = {
    #         # # with old TARS G4 app (using MicroElec)
    #         # 'E$_{init?}$, TARS (G4app), interpol., lin. sampl.':
    #         #     Path(r'C:\dev\work\tars-old-validation\validation' +
    #         #          r'\G4_app_results_20180425\tars-p_energy_lst_per_event.npy'),
    #         # 10k
    #         r'E$_{init}$, TARS (stepsize), no interpol.':
    #             Path(r'C:\dev\work\pyxel\tars_p_init_energy_lst_per_event_10k_v7.npy'),
    #         # 10k
    #         r'E$_{final}$, TARS (stepsize), no interpol.':
    #             Path(r'C:\dev\work\pyxel\tars_p_final_energy_lst_per_event_10k_v7.npy'),
    #
    #         # latest
    #         r'E$_{init}$, TARS (stepsize) latest':
    #             Path(r'C:\dev\work\pyxel\tars_p_init_energy_lst_per_event.npy'),
    #         # latest
    #         r'E$_{final}$, TARS (stepsize) latest':
    #             Path(r'C:\dev\work\pyxel\tars_p_final_energy_lst_per_event.npy')
    #     }
    #     for label, filename in hist_names.items():
    #         histogram_data = np.load(filename)
    #         col = None
    #         plt.hist(histogram_data, bins=hist_bins, range=hist_range, log=log,
    #                  histtype='step', label=label, color=col)
    #     plt.gca().set_xscale("log")
    #     plt.legend(loc='upper right')
    #     self.save_and_draw('tars_hist_initial_final_proton_spectra')

    def event_polar_angle_dist(self, alpha, beta):
        """TBW."""
        if isinstance(alpha, str):
            if alpha.endswith('.npy'):
                alpha = np.load(alpha)
        if isinstance(beta, str):
            if beta.endswith('.npy'):
                beta = np.load(beta)
        fig = plt.figure()
        fig.add_subplot(111, polar=True)
        plt.hist(alpha, bins=360, histtype='step', label='alpha')
        plt.hist(beta, bins=360, histtype='step', label='beta')
        plt.legend()
        plt.title('Incident angle distributions')
        plt.xlabel('')
        plt.ylabel('')
        self.save_and_draw('event_angles')

    def cluster_charge_number(self, chg_num):
        """TBW."""
        if isinstance(chg_num, str):
            if chg_num.endswith('.npy'):
                chg_num = np.load(chg_num, allow_pickle=True)
        all_charge_cluster = []
        for chg_list in chg_num:
            all_charge_cluster += list(chg_list)
        plt.figure()
        plt.hist(all_charge_cluster, bins=100, histtype='step')
        plt.title('Charge number per cluster')
        plt.xlabel('[e-]')
        plt.ylabel('')
        self.save_and_draw('cluster_charge_number')

    def cluster_positions(self, chg_v_pos, chg_h_pos, chg_z_pos):
        """TBW."""
        if isinstance(chg_v_pos, str):
            if chg_v_pos.endswith('.npy'):
                chg_v_pos = np.load(chg_v_pos, allow_pickle=True)
        if isinstance(chg_h_pos, str):
            if chg_h_pos.endswith('.npy'):
                chg_h_pos = np.load(chg_h_pos, allow_pickle=True)
        if isinstance(chg_z_pos, str):
            if chg_z_pos.endswith('.npy'):
                chg_z_pos = np.load(chg_z_pos, allow_pickle=True)
        all_cluster_v_pos = []
        all_cluster_h_pos = []
        all_cluster_z_pos = []
        for v, h, z in zip(chg_v_pos, chg_h_pos, chg_z_pos):
            all_cluster_v_pos += list(v)
            all_cluster_h_pos += list(h)
            all_cluster_z_pos += list(z)
        plt.figure()
        plt.hist(all_cluster_v_pos, bins=100, histtype='step', label='vertical')
        plt.hist(all_cluster_h_pos, bins=100, histtype='step', label='horizontal')
        plt.legend()
        plt.title('Cluster positions')
        plt.xlabel('v, h [um]')
        plt.ylabel('')
        self.save_and_draw('cluster_positions_yx')
        plt.figure()
        plt.hist(all_cluster_z_pos, bins=100, color='g', histtype='step', label='z')
        plt.legend()
        plt.title('Cluster positions')
        plt.xlabel('z [um]')
        plt.ylabel('')
        self.save_and_draw('cluster_positions_z')

    def event_direction_hist(self, direction):
        """TBW."""
        if isinstance(direction, str):
            if direction.endswith('.npy'):
                direction = np.load(direction)
        plt.figure()
        plt.hist(direction[:, 0], bins=100, histtype='step', label='vert')
        plt.hist(direction[:, 1], bins=100, histtype='step', label='horz')
        plt.hist(direction[:, 2], bins=100, histtype='step', label='z')
        plt.legend()
        plt.title('Direction per event')
        plt.xlabel('')
        plt.ylabel('')
        self.save_and_draw('event_direction')

    def geometry_3d(self, margin=1, show_only_det=True):
        """TBW."""
        fig = plt.figure(figsize=plt.figaspect(1.))
        # fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        point1 = np.array([0, 0, 0])
        point2 = np.array([0, 0, -1 * self.geometry['det_total_thickness']])
        normal = np.array([0, 0, 1])
        d1 = -point1.dot(normal)
        d2 = -point2.dot(normal)
        xx, yy = np.meshgrid(np.linspace(0, self.geometry['det_vert_dimension'], 10),
                             np.linspace(0, self.geometry['det_horz_dimension'], 10))
        z1 = (-normal[0] * xx - normal[1] * yy - d1) * 1. / normal[2]
        z2 = (-normal[0] * xx - normal[1] * yy - d2) * 1. / normal[2]
        ax.plot_surface(xx, yy, z1, alpha=0.2, color=(0, 0, 1))
        ax.plot_surface(xx, yy, z2, alpha=0.2, color=(0, 0, 1))
        if show_only_det:
            ax.set_xlim(-1 * margin, self.geometry['det_vert_dimension'] + margin)
            ax.set_ylim(-1 * margin, self.geometry['det_horz_dimension'] + margin)
            ax.set_zlim(-1 * self.geometry['det_total_thickness'] - margin, margin)
        else:
            max_dimension = max(self.geometry['det_vert_dimension'], self.geometry['det_horz_dimension'])
            ax.set_xlim(-1 * margin, max_dimension + margin)
            ax.set_ylim(-1 * margin, max_dimension + margin)
            ax.set_zlim(-1 * max_dimension/2 - margin, max_dimension/2 + margin)
        ax.set_xlabel(r'vertical [$\mu$m]')
        ax.set_ylabel(r'horizontal [$\mu$m]')
        ax.set_zlabel(r'z [$\mu$m]')

    def event_tracks_3d(self, first_pos, last_pos):
        """TBW."""
        if isinstance(first_pos, str):
            if first_pos.endswith('.npy'):
                first_pos = np.load(first_pos)
        if isinstance(last_pos, str):
            if last_pos.endswith('.npy'):
                last_pos = np.load(last_pos)
        self.geometry_3d(show_only_det=True)
        ax = plt.gca()
        for first, last in zip(first_pos, last_pos):
            ax.plot([first[0], last[0]],
                    [first[1], last[1]],
                    [first[2], last[2]],
                    'x-', c='r')
        plt.title('Event tracks')
        self.save_and_draw('event_tracks_3d')

    def cluster_charges_3d(self, chg_v_pos, chg_h_pos, chg_z_pos, chg_num):
        """TBW."""
        if isinstance(chg_v_pos, str):
            if chg_v_pos.endswith('.npy'):
                chg_v_pos = np.load(chg_v_pos, allow_pickle=True)
        if isinstance(chg_h_pos, str):
            if chg_h_pos.endswith('.npy'):
                chg_h_pos = np.load(chg_h_pos, allow_pickle=True)
        if isinstance(chg_z_pos, str):
            if chg_z_pos.endswith('.npy'):
                chg_z_pos = np.load(chg_z_pos, allow_pickle=True)
        if isinstance(chg_num, str):
            if chg_num.endswith('.npy'):
                chg_num = np.load(chg_num, allow_pickle=True)
        self.geometry_3d(show_only_det=True)
        ax = plt.gca()
        for v, h, z, s in zip(chg_v_pos, chg_h_pos, chg_z_pos, chg_num):
            cluster_sizes = [k / 10. for k in s]
            ax.scatter(v, h, z, c='b', marker='.', s=cluster_sizes)
        plt.title('Cluster positions and sizes in 3d')
        self.save_and_draw('cluster_charges_3d')

    def event_energy_deposited(self, edep):
        """TBW."""
        if isinstance(edep, str):
            if edep.endswith('.npy'):
                edep = np.load(edep)
        plt.figure()
        plt.hist(edep, bins=200, histtype='step', label='edep')
        plt.legend()
        plt.title('Energy deposited per event')
        plt.xlabel('[keV]')
        plt.ylabel('')
        self.save_and_draw('event_energy_deposited')

    def event_electrons_deposited(self, elec):
        """TBW."""
        if isinstance(elec, str):
            if elec.endswith('.npy'):
                elec = np.load(elec)
        plt.figure()
        plt.hist(elec, bins=200, histtype='step', label='elec')
        plt.legend()
        plt.title('Electrons deposited per event')
        plt.xlabel('[e-]')
        plt.ylabel('')
        self.save_and_draw('event_electrons_deposited')

    def event_proton_spectra(self, init=None, final=None, groups=None):
        """TBW."""
        if init is not None:
            if isinstance(init, str):
                if init.endswith('.npy'):
                    init = np.load(init)
        if final is not None:
            if isinstance(final, str):
                if final.endswith('.npy'):
                    final = np.load(final)
        if groups is not None:
            if isinstance(groups, str):
                if groups.endswith('.csv'):
                    import pandas as pd
                    groups = pd.read_csv(groups)
                    groups = np.unique(groups['energy'].values)
        plt.figure()
        bins = 400
        lbd, ubd = 1., 10000.       # MeV

        if init is not None:
            plt.hist(init,
                     bins=np.logspace(np.log10(lbd), np.log10(ubd), bins),
                     histtype='step', label='initial')
        if final is not None:
            plt.hist(final,
                     bins=np.logspace(np.log10(np.min(lbd)), np.log10(np.max(ubd)), bins),
                     histtype='step', label='final')
        if groups is not None:
            plt.hist(groups,
                     bins=np.logspace(np.log10(np.min(lbd)), np.log10(np.max(ubd)), bins),
                     histtype='step', label='%d energy groups' % groups.size)

        plt.gca().set_xscale("log")
        plt.legend()
        plt.title('Proton spectrum')
        plt.xlabel('energy [MeV]')
        plt.ylabel('')
        self.save_and_draw('event_proton_spectrum')

    def event_starting_position(self, start_pos):
        """TBW."""
        if isinstance(start_pos, str):
            if start_pos.endswith('.npy'):
                start_pos = np.load(start_pos)
        self.geometry_3d(margin=5, show_only_det=False)
        ax = plt.gca()
        ax.scatter(start_pos[:, 0], start_pos[:, 1], start_pos[:, 2], marker='*')
        plt.title('Proton starting position')
        self.save_and_draw('event_starting_position')

    def event_track_length(self, track):
        """TBW."""
        if isinstance(track, str):
            if track.endswith('.npy'):
                track = np.load(track)
        plt.figure()
        plt.hist(track, bins=200, range=(0, 200), histtype='step', label='track')
        plt.legend()
        plt.title('Track length per event')
        plt.xlabel(r'[$\mu$m]')
        plt.ylabel('')
        self.save_and_draw('event_track_length')

    def cluster_step_size(self, step_size):
        """TBW."""
        if isinstance(step_size, str):
            if step_size.endswith('.npy'):
                step_size = np.load(step_size)
        plt.figure()
        plt.hist(step_size,
                 bins=np.logspace(np.log10(np.min(step_size)), np.log10(np.max(step_size)), 100),
                 histtype='step', label='step size')
        plt.gca().set_xscale("log")
        plt.legend()
        plt.title('Step size per cluster')
        plt.xlabel(r'[$\mu$m]')
        plt.ylabel('')
        self.save_and_draw('cluster_step_size')

    def plato_particle_contribution(self):
        """TBW."""

        path = Path(__file__).parent.joinpath('data', 'validation')

        # x = [10000, 1000, 1000, 2000, 3000, 1000, 10000, 4000]
        # g4file = Path(path, 'PLATO_irrad_proton_spectrum_15um_Silicon_10000_MicroElec.ascii')
        # # plato_spectrum_step_size = load_geant4_histogram(g4file, hist_type='step_size', skip_rows=4, read_rows=x[0])
        # plato_spectrum_all_elec = load_geant4_histogram(g4file, hist_type='elec', skip_rows=sum(x[:7]) + 4 * 8,
        #                                                 read_rows=x[7])
        # plato_spectrum_all_edep = load_geant4_histogram(g4file, hist_type='edep', skip_rows=sum(x[:6]) + 4 * 7,
        #                                                 read_rows=x[6])
        #
        # g4file = Path(__file__).parent.joinpath('data', 'diff_thick_new',
        #                                         'stepsize_proton_55MeV_15um_Silicon_10000_MicroElec.ascii')
        # # geant4_step_size = load_geant4_histogram(g4file, hist_type='step_size', skip_rows=4, read_rows=x[0])
        # geant4_all_elec = load_geant4_histogram(g4file, hist_type='elec', skip_rows=sum(x[:7]) + 4 * 8, read_rows=x[7])
        # geant4_all_edep = load_geant4_histogram(g4file, hist_type='edep', skip_rows=sum(x[:6]) + 4 * 7, read_rows=x[6])

        plato_data_array = np.loadtxt(str(
            Path(__file__).parent.joinpath('data', 'validation', 'CosmicsStatsplato-cold-irrad-protons.txt')))

        x = [10000, 1000, 1000, 2000, 3000, 1000, 10000, 4000]
        g4file = Path(path, 'PLATO_irrad_proton_spectrum_15um_Silicon_10000_MicroElec.ascii')
        spectrum_p_uelec_all_elec = load_geant4_histogram(g4file, hist_type='all_elec', skip_rows=sum(x[:7]) + 4 * 8,
                                                          read_rows=x[7])
        x = [10000, 1000, 1000, 2000, 3000, 1000, 1000, 4000]
        g4file = Path(path, 'PLATO_irrad_e-_spectrum_15um_Silicon_10000_MicroElec.ascii')
        spectrum_e_uelec_all_elec = load_geant4_histogram(g4file, hist_type='all_elec', skip_rows=sum(x[:7]) + 4 * 8,
                                                          read_rows=x[7])
        # x = [10000, 1000, 1000, 2000, 3000, 1000, 1000, 4000]
        # g4file = Path(path, 'PLATO_irrad_e-_spectrum_15um_Silicon_10000_EMopt4.ascii')
        # spectrum_e_emopt4_all_elec = load_geant4_histogram(g4file, hist_type='all_elec', skip_rows=sum(x[:7]) + 4 * 8,
        #                                                   read_rows=x[7])

        import matplotlib
        font = {'size': 14}
        matplotlib.rc('font', **font)

        fig = plt.figure(figsize=(8, 5))
        hrange = (0, 20000)
        title = 'Deposited electrons per event, PLATO CCD'
        density = False

        plato_data = load_data_into_histogram(plato_data_array, plato=True, lim=hrange)
        histbins = plato_data[:, 0]
        sum_data = np.sum(plato_data[:, 1])
        # plato_data[:, 1] /= np.max(plato_data[:, 1])
        plato_data[:, 1] /= sum_data
        sum_data = np.sum(plato_data[:, 1])

        plt.hist(plato_data[:, 0], bins=histbins, weights=plato_data[:, 1], histtype='stepfilled',
                 density=density, linewidth=2, color='blue', label='PLATO CCD data', alpha=0.2)

        # proton_factor = 9.942500e+00
        # electron_factor = 6.162000e-01
        proton_factor = 0.93
        electron_factor = 0.07

        protons = load_data_into_histogram(spectrum_p_uelec_all_elec.values, plato=False, regrp=None, lim=hrange)
        sum_protons = np.sum(protons[:, 1])
        proton_factor = sum_data / sum_protons * proton_factor
        protons[:, 1] *= proton_factor

        plt.hist(protons[:, 0], bins=histbins, weights=protons[:, 1], histtype='step', color='red', linewidth=1.4,
                 density=density, label='G4: p (93%)')  # label='G4: p w/ spectrum (93%)')  #, alpha=0.8)

        electrons = load_data_into_histogram(spectrum_e_uelec_all_elec.values, plato=False, regrp=None, lim=hrange)
        sum_electrons = np.sum(electrons[:, 1])
        electron_factor = sum_data / sum_electrons * electron_factor
        electrons[:, 1] *= electron_factor

        plt.hist(electrons[:, 0], bins=histbins, weights=electrons[:, 1], histtype='step', color='C0', linewidth=1.4,
                 density=density, label='G4: e (7%)') # label='G4: e w/ spectrum (7%)')  #, alpha=0.8)

        # electrons2 = load_data_into_histogram(spectrum_e_emopt4_all_elec.values, plato=False, regrp=None, lim=hrange)
        # plt.hist(electrons2[:, 0], bins=histbins, weights=electrons2[:, 1], histtype='step',
        #          density=True, label='G4 EMopt4, spectrum, only electrons', alpha=1)

        # total = protons
        # total[:, 1] = protons[:, 1] + electrons[:, 1]
        # plt.hist(total[:, 0], bins=histbins, weights=total[:, 1], histtype='step',
        #          density=density, alpha=1,
        #          label=r'%.1f p + %.2f e' % (proton_factor, electron_factor))

        plt.title(title)
        plt.xlabel(r'electrons (e$^-$)')
        plt.ylabel('normalized counts')
        plt.legend()
        # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 1))
        fig.tight_layout()
        self.save_and_draw('plato-data-protons-vs-electrons')

    def plato_histograms(self):
        """TBW."""

        # path = Path(__file__).parent.joinpath('data', 'validation')
        # x = [10000, 1000, 1000, 2000, 3000, 1000, 10000, 4000]
        # g4file = Path(path, 'PLATO_irrad_proton_spectrum_15um_Silicon_10000_MicroElec.ascii')
        # plato_spectrum_all_elec = load_geant4_histogram(g4file, hist_type='elec', skip_rows=sum(x[:7]) + 4 * 8,
        #                                                 read_rows=x[7])
        # plato_spectrum_all_edep = load_geant4_histogram(g4file, hist_type='edep', skip_rows=sum(x[:6]) + 4 * 7,
        #                                                 read_rows=x[6])

        # g4file = Path(__file__).parent.joinpath('data', 'diff_thick_new',
        #                                         'stepsize_proton_55MeV_15um_Silicon_10000_MicroElec.ascii')
        # geant4_all_elec = load_geant4_histogram(g4file, hist_type='elec', skip_rows=sum(x[:7]) + 4 * 8, read_rows=x[7])
        # geant4_all_edep = load_geant4_histogram(g4file, hist_type='edep', skip_rows=sum(x[:6]) + 4 * 7, read_rows=x[6])

        plato_data_array = np.loadtxt(str(
            Path(__file__).parent.joinpath('data', 'validation', 'CosmicsStatsplato-cold-irrad-protons.txt')))

        import matplotlib
        font = {'size': 14}
        matplotlib.rc('font', **font)

        # fig = plt.figure(figsize=(8, 6))
        # hrange = (0, 100)  # keV
        # title = 'Total energy deposited per event'
        # density = True
        # regrouping_factor = 100
        #
        # geant4_all_edep = load_data_into_histogram(geant4_all_edep.values, plato=False, lim=hrange,
        #                                            regrp=regrouping_factor)
        # # plato_spectrum_all_edep = load_data_into_histogram(plato_spectrum_all_edep.values, plato=False, lim=hrange)
        #
        # hbins_edep = geant4_all_edep[:, 0] * 1000
        #
        # plt.hist(geant4_all_edep[:, 0] * 1000, bins=hbins_edep, weights=geant4_all_edep[:, 1],
        #          density=density, histtype='step', label=r'G4: p, $55\,MeV, 15\,\mu m$', alpha=1.)
        # # plt.hist(plato_spectrum_all_edep[:, 0] * 1000, bins=hbins_edep, weights=plato_spectrum_all_edep[:, 1],
        # #          density=density, histtype='step', label=r'G4: p, spectrum, $15\,\mu m$', alpha=1.)
        #
        # for key, value in edep.items():
        #     if isinstance(value, str):
        #         if value.endswith('.npy'):
        #             cosmix_edep = np.load(value)
        #             plt.hist(cosmix_edep, bins=hbins_edep, range=hrange,
        #                      density=density, histtype='step', label=r'CosmiX: p, $55\,MeV$' + str(key))
        #
        # plt.title(title)
        # plt.xlabel('energy (keV)')
        # if density:
        #     plt.ylabel('normalized counts')
        # else:
        #     plt.ylabel('counts')
        # plt.legend()
        # fig.tight_layout()
        # self.save_and_draw('plato-edep-different-char-lengths')

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        fig = plt.figure(figsize=(8, 5))
        hrange = (3500, 20000)
        plato_data_hrange = (3500, 20000)       # cut down the electron contribution
        title = 'Deposited electrons per event, PLATO CCD'
        density = False
        regrouping_factor = 2
        # regrouping_factor = None

        plato_data = load_data_into_histogram(plato_data_array, plato=True,
                                              lim=plato_data_hrange, regrp=regrouping_factor)
        plato_hbins = load_data_into_histogram(plato_data_array, plato=True,
                                               lim=hrange, regrp=regrouping_factor)
        hbins_elec = plato_hbins[:, 0]

        # PLATO DATA NORMALISATION
        sum_data = np.sum(plato_data[:, 1])
        plato_data[:, 1] /= sum_data
        sum_data = np.sum(plato_data[:, 1])

        # col = 'green'
        um = r'$\,\mu m$'

        # COSMIX HISTOS
        cosmix_elec_2 = np.load('outputs/PLATO/runs_55MeV_20k/out_2um/cosmix_electron_per_event.npy')
        cosmix_elec_2, _, _ = plt.hist(cosmix_elec_2, bins=hbins_elec, range=hrange, density=density)
        cosmix_elec_4 = np.load('outputs/PLATO/runs_55MeV_20k/out_4um/cosmix_electron_per_event.npy')
        cosmix_elec_4, _, _ = plt.hist(cosmix_elec_4, bins=hbins_elec, range=hrange, density=density)
        cosmix_elec_15 = np.load('outputs/PLATO/runs_55MeV_20k/out_15um/cosmix_electron_per_event.npy')
        cosmix_elec_15, _, _ = plt.hist(cosmix_elec_15, bins=hbins_elec, range=hrange, density=density)
        fig.clear()

        # PLATO DATA PLOT
        plt.hist(plato_data[:, 0], bins=hbins_elec, weights=plato_data[:, 1], histtype='stepfilled',
                 density=density, linewidth=2, color='blue', label='PLATO CCD data', alpha=0.2)

        # COSMIX NORMALISATIONS AND PLOTS
        # == 2 um ==
        proton_factor = 0.93
        sum_csmx_protons = np.sum(cosmix_elec_2)
        pf = sum_data / sum_csmx_protons * proton_factor
        cosmix_elec_2 *= pf
        plt.hist(hbins_elec[:-1], bins=hbins_elec, weights=cosmix_elec_2, range=hrange, linewidth=1.6,  # color=col,
                 density=density, histtype='step', label='CosmiX: p (%d' % int(proton_factor*100) +
                                                         r'%), $l_{char}=2$' + um)
                                                         # r'%), $55\,MeV$, $l_{char}=2$' + um)
        # == 4 um ==
        proton_factor = 0.93
        sum_csmx_protons = np.sum(cosmix_elec_4)
        pf = sum_data / sum_csmx_protons * proton_factor
        cosmix_elec_4 *= pf
        plt.hist(hbins_elec[:-1], bins=hbins_elec, weights=cosmix_elec_4, range=hrange, linewidth=1.6,  # color=col,
                 density=density, histtype='step', label='CosmiX: p (%d' % int(proton_factor*100) +
                                                         r'%), $l_{char}=4$' + um)
                                                         # r'%), $55\,MeV$, $l_{char}=4$' + um)
        # == 15 um ==
        proton_factor = 0.93
        sum_csmx_protons = np.sum(cosmix_elec_15)
        pf = sum_data / sum_csmx_protons * proton_factor
        cosmix_elec_15 *= pf
        plt.hist(hbins_elec[:-1], bins=hbins_elec, weights=cosmix_elec_15, range=hrange, linewidth=1.6,  # color=col,
                 density=density, histtype='step', label='CosmiX: p (%d' % int(proton_factor*100) +
                                                         r'%), $l_{char}=15$' + um)
                                                         # r'%), $55\,MeV$, $l_{char}=15$' + um)

        plt.xlim(plato_data_hrange)
        plt.title(title)
        plt.xlabel(r'electrons (e$^-$)')
        plt.ylabel('normalized counts')
        plt.legend()
        # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 1))
        fig.tight_layout()
        self.save_and_draw('plato-elec-different-char-lengths')

    def check_geant4_distributions(self, files: dict):
        """TBW."""

        # import matplotlib
        # font = {'size': 14}
        # matplotlib.rc('font', **font)

        fig = plt.figure(figsize=(8, 6))
        hrange = (0, 100)  # keV
        title = 'Total energy deposited per event, Geant4'
        density = True
        regrouping_factor = 50

        x = [10000, 1000, 1000, 2000, 3000, 1000, 10000, 4000]

        for key, g4file in files.items():
            if isinstance(g4file, str):

                # geant4_all_elec = load_geant4_histogram(g4file, hist_type='elec',
                #                                         skip_rows=sum(x[:7]) + 4 * 8, read_rows=x[7])
                geant4_all_edep = load_geant4_histogram(g4file, hist_type='edep',
                                                        skip_rows=sum(x[:6]) + 4 * 7, read_rows=x[6])

                geant4_all_edep = load_data_into_histogram(geant4_all_edep.values, plato=False, lim=hrange,
                                                           regrp=regrouping_factor)
                hbins_edep = geant4_all_edep[:, 0] * 1000

                plt.hist(hbins_edep, bins=hbins_edep, weights=geant4_all_edep[:, 1],
                         density=density, histtype='step', label='G4 ' + str(key), alpha=1.)

        plt.title(title)
        plt.xlabel('energy (keV)')
        if density:
            plt.ylabel('normalized counts')
        else:
            plt.ylabel('counts')
        plt.legend()
        fig.tight_layout()
        self.save_and_draw('geant4-edep-different-energy')

    def gaia_bam_histograms(self):
        """TBW."""

        import matplotlib
        font = {'size': 14}
        matplotlib.rc('font', **font)
        um = r'$\,\mu m$'
        fig = plt.figure(figsize=(8, 5))
        hrange = (0, 20000)
        gaia_data_bins = 100
        gaia_data_range = (0, 20000)       # cut down the electron contribution
        title = 'Deposited electrons per event, BAM CCD (40' + um + ')'
        density = False
        # density = True

        path = Path(__file__).parent.joinpath('data', 'validation', 'GAIA-DATA')

        # ===== CREATE HISTOS =====
        gaia_bam_data = np.load(Path(path, 'Gaia_CCD_Data-20180404T115340Z-001', 'CRs_from_BAM_Gaia_CCDs.npy'))
        hist_weigth, hist_bins, _ = plt.hist(gaia_bam_data, bins=gaia_data_bins, range=gaia_data_range, density=density)
        cosmix_elec_2 = np.load('outputs/GAIA/BAM_new/BAM-2um/cosmix_electron_per_event.npy')
        # cosmix_elec_2 = np.load('outputs/GAIA/BAM_40um/2um/cosmix_electron_per_event.npy')
        cos_el_2_weight, _, _ = plt.hist(cosmix_elec_2, bins=hist_bins, range=hrange, density=density)
        cosmix_elec_10 = np.load('outputs/GAIA/BAM_new/BAM-10um/cosmix_electron_per_event.npy')
        # cosmix_elec_10 = np.load('outputs/GAIA/BAM_40um/10um/cosmix_electron_per_event.npy')
        cos_el_10_weight, _, _ = plt.hist(cosmix_elec_10, bins=hist_bins, range=hrange, density=density)
        fig.clear()

        # ===== NORMALISATION =====
        sum_data = np.sum(hist_weigth)
        hist_weigth /= sum_data
        sum_data = np.sum(hist_weigth)

        # ===== PLOTTING =====
        # GAIA BAM DATA
        _, hist_bins, _ = plt.hist(hist_bins[:-1], bins=hist_bins, weights=hist_weigth, range=gaia_data_range,
                                   histtype='stepfilled', density=density, linewidth=2, alpha=0.4,
                                   color='purple', label='Gaia BAM in-orbit data')

        col = 'red'

        # COSMIX 2 um
        proton_factor = 0.695647     # 1.  # 0.67
        sum_csmx_protons = np.sum(cos_el_2_weight)
        proton_factor = sum_data / sum_csmx_protons * proton_factor
        cos_el_2_weight *= proton_factor
        plt.hist(hist_bins[:-1], bins=hist_bins, range=hrange, weights=cos_el_2_weight,
                 linewidth=1.6, color=col, alpha=0.8, density=density, histtype='step',
                 label=r'CosmiX: p (69.6%), $l_{char}$=2' + um)

        # COSMIX 10 um
        proton_factor = 0.695647    # 1.  # 0.67
        sum_csmx_protons = np.sum(cos_el_10_weight)
        proton_factor = sum_data / sum_csmx_protons * proton_factor
        cos_el_10_weight *= proton_factor
        plt.hist(hist_bins[:-1], bins=hist_bins, range=hrange, weights=cos_el_10_weight,
                 linewidth=1.6, color=col, alpha=0.4, density=density, histtype='step',
                 label=r'CosmiX: p (69.6%), $l_{char}$=10' + um)

        from util import read_data
        # COSMIX_EDEP_HIST_R.out
        gras_cosmix_data = read_data(Path(path, 'my', 'COSMIX_EDEP_HIST_R.out'))
        proton_factor = 0.695647    # 1.
        sum_csmx_protons = np.sum(gras_cosmix_data[:, 1])
        proton_factor = sum_data / sum_csmx_protons * proton_factor
        gras_cosmix_data[:, 1] *= proton_factor
        # plt.hist(gras_cosmix_data[:, 0], bins=hist_bins, range=hrange, weights=gras_cosmix_data[:, 1],
        #          linewidth=1.6, alpha=0.8, density=density,  histtype='step',
        #          label=r'GRAS, COSMIX, BAM/R')

        # # ANTI_COSMIX_EDEP_HIST_R.out
        # gras_anti_cosmix_data = read_data(Path(path, 'my', 'ANTI_COSMIX_EDEP_HIST_R.out'))
        # proton_factor = 0.304353   # 1.
        # sum_csmx_protons = np.sum(gras_anti_cosmix_data[:, 1])
        # proton_factor = sum_data / sum_csmx_protons * proton_factor
        # gras_anti_cosmix_data[:, 1] *= proton_factor
        # plt.hist([gras_cosmix_data[:, 0], gras_anti_cosmix_data[:, 0]],
        #          bins=hist_bins, range=hrange,
        #          weights=[gras_cosmix_data[:, 1], gras_anti_cosmix_data[:, 1]],
        #          linewidth=1.6, alpha=0.4, density=density, stacked=True,
        #          label=[r'GRAS, COSMIX, BAM/R', r'GRAS, ANTI COSMIX, BAM/R'])

        # ANTI_COSMIX_EDEP_HIST_R.out
        gras_anti_cosmix_data = read_data(Path(path, 'my', 'ANTI_COSMIX_EDEP_HIST_R.out'))
        proton_factor = 0.304353   # 1.
        sum_csmx_protons = np.sum(gras_anti_cosmix_data[:, 1])
        proton_factor = sum_data / sum_csmx_protons * proton_factor
        gras_anti_cosmix_data[:, 1] *= proton_factor
        plt.hist(gras_anti_cosmix_data[:, 0], bins=hist_bins, range=hrange,
                 weights=gras_anti_cosmix_data[:, 1], histtype='step',
                 linewidth=1.6, alpha=0.6, density=density,
                 label=r'GRAS: secondaries+$\alpha$ (30.4%)')

        plt.title(title)
        plt.xlabel(r'electrons (e$^-$)')
        plt.ylabel('normalized counts')
        plt.legend(loc='upper right')
        # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 1))
        fig.tight_layout()
        self.save_and_draw('gaia-bam-cosmix-elec-histograms')

    def gaia_sm_histograms(self):
        """TBW."""

        import matplotlib
        font = {'size': 14}
        matplotlib.rc('font', **font)
        um = r'$\,\mu m$'
        fig = plt.figure(figsize=(8, 5))
        hrange = (0, 20000)
        gaia_data_bins = 100
        gaia_data_range = (0, 20000)       # cut down the electron contribution
        title = 'Deposited electrons per event, SM CCD (16' + um + ')'
        # density = True
        density = False

        path = Path(__file__).parent.joinpath('data', 'validation', 'GAIA-DATA')

        # GAIA IN-ORBIT DATA IN ELECTRONS:
        # gaia_sm_data = np.load(Path(path, 'Gaia_CCD_Data-20180404T115340Z-001', 'CRs_from_SM_Gaia_CCDs.npy'))
        # _, hist_bins, _ = plt.hist(gaia_sm_data, bins=gaia_data_bins, range=gaia_data_range, histtype='stepfilled', color='red',
        #                            label='Gaia SM in-orbit data', density=density, linewidth=2, alpha=0.4)

        # ===== CREATE HISTOS =====
        gaia_sm_data = np.load(Path(path, 'Gaia_CCD_Data-20180404T115340Z-001', 'CRs_from_SM_Gaia_CCDs.npy'))
        hist_weigth, hist_bins, _ = plt.hist(gaia_sm_data, bins=gaia_data_bins, range=gaia_data_range, density=density)
        cosmix_elec_2 = np.load('outputs/GAIA/SM_new/SM-2um/cosmix_electron_per_event.npy')
        # cosmix_elec_2 = np.load('outputs/GAIA/SM_16um/2um/cosmix_electron_per_event.npy')
        cos_el_2_weight, _, _ = plt.hist(cosmix_elec_2, bins=hist_bins, range=hrange, density=density)
        cosmix_elec_10 = np.load('outputs/GAIA/SM_new/SM-10um/cosmix_electron_per_event.npy')
        # cosmix_elec_10 = np.load('outputs/GAIA/SM_16um/10um/cosmix_electron_per_event.npy')
        cos_el_10_weight, _, _ = plt.hist(cosmix_elec_10, bins=hist_bins, range=hrange, density=density)
        fig.clear()

        # ===== NORMALISATION =====
        sum_data = np.sum(hist_weigth)
        hist_weigth /= sum_data
        sum_data = np.sum(hist_weigth)

        # ===== PLOTTING =====
        # GAIA SM DATA
        _, hist_bins, _ = plt.hist(hist_bins[:-1], bins=hist_bins, weights=hist_weigth, range=gaia_data_range,
                                   histtype='stepfilled', density=density, linewidth=2, alpha=0.4,
                                   color='red', label='Gaia SM in-orbit data')

        col = 'purple'

        # COSMIX 2 um
        proton_factor = 0.695647   # 1.  # 0.67
        sum_csmx_protons = np.sum(cos_el_2_weight)
        proton_factor = sum_data / sum_csmx_protons * proton_factor
        cos_el_2_weight *= proton_factor
        plt.hist(hist_bins[:-1], bins=hist_bins, range=hrange, weights=cos_el_2_weight,
                 linewidth=1.6, color=col, alpha=0.8, density=density, histtype='step',
                 label=r'CosmiX: p (69.6%), $l_{char}$=2' + um)

        # COSMIX 10 um
        proton_factor = 0.695647    # 1.  # 0.67
        sum_csmx_protons = np.sum(cos_el_10_weight)
        proton_factor = sum_data / sum_csmx_protons * proton_factor
        cos_el_10_weight *= proton_factor
        plt.hist(hist_bins[:-1], bins=hist_bins, range=hrange, weights=cos_el_10_weight,
                 linewidth=1.6, color=col, alpha=0.4, density=density, histtype='step',
                 label=r'CosmiX: p (69.6%), $l_{char}$=10' + um)

        plt.title(title)
        plt.xlabel(r'electrons (e$^-$)')
        plt.ylabel('normalized counts')
        plt.legend(loc='upper right')
        # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 1))
        fig.tight_layout()
        self.save_and_draw('gaia-sm-cosmix-elec-histograms')

    def gaia_only_data_histograms(self):
        """TBW."""

        import matplotlib
        font = {'size': 14}
        matplotlib.rc('font', **font)

        # fig = plt.figure(figsize=(8, 6))
        fig = plt.figure(figsize=(8, 5))
        # hrange = (1, 20000)

        gaia_data_bins = 150
        gaia_data_range = (1, 15000)       # cut down the electron contribution
        title = 'Deposited electrons per event, Gaia CCDs'
        density = False
        # density = True

        path = Path(__file__).parent.joinpath('data', 'validation', 'GAIA-DATA')

        # GAIA IN-ORBIT DATA IN ELECTRONS:
        # GAIA SM DATA
        gaia_sm_data = np.load(Path(path, 'Gaia_CCD_Data-20180404T115340Z-001', 'CRs_from_SM_Gaia_CCDs.npy'))
        gaia_sm_weight, hist_bins, _ = plt.hist(gaia_sm_data, bins=gaia_data_bins, range=gaia_data_range)
        # GAIA BAM DATA
        gaia_bam_data = np.load(Path(path, 'Gaia_CCD_Data-20180404T115340Z-001', 'CRs_from_BAM_Gaia_CCDs.npy'))
        gaia_bam_weight, _, _ = plt.hist(gaia_bam_data, bins=gaia_data_bins, range=gaia_data_range)
        fig.clear()
        # SM NORMALISATION & PLOT
        sum_data = np.sum(gaia_sm_weight)
        gaia_sm_weight /= sum_data
        sum_data = np.sum(gaia_sm_weight)
        plt.hist(hist_bins[:-1], bins=hist_bins, range=gaia_data_range, weights=gaia_sm_weight,
                 histtype='stepfilled', density=density, linewidth=2, alpha=0.4, color='red',
                 label='Gaia SM in-orbit data')
        # BAM NORMALISATION & PLOT
        sum_bam = np.sum(gaia_bam_weight)
        gaia_bam_weight *= sum_data / sum_bam
        plt.hist(hist_bins[:-1], bins=hist_bins, range=gaia_data_range, weights=gaia_bam_weight,
                 histtype='stepfilled', density=density, linewidth=2, alpha=0.4, color='purple',
                 label='Gaia BAM in-orbit data')

        # # GRAS SIMULATION:
        # gras_data = np.load(Path(path, 'Gaia_CCD_Data-20180404T115340Z-001', 'complete_G4_H_He_GCR_sim_deposition.npy'))
        # plt.hist(gras_data, bins=hist_bins, range=gaia_data_range, histtype='step', color='orange',
        #          label=r'GRAS: p+$\alpha$+secondaries, BAM', density=density, linewidth=1.8, alpha=1.)

        from util import read_data
        gras_data = read_data(Path(path, 'my', 'hedepperevent_all_R.out'))
        sum_gras = np.sum(gras_data[:, 1])
        gras_data[:, 1] *= sum_data / sum_gras
        plt.hist(gras_data[:, 0], bins=hist_bins, weights=gras_data[:, 1], histtype='step', color='brown',
                 label=r'GRAS: p+$\alpha$+secondaries, BAM/R', density=density, linewidth=1.6, alpha=0.8)

        gras_data = read_data(Path(path, 'my', 'hedepperevent_all_N.out'))
        sum_gras = np.sum(gras_data[:, 1])
        gras_data[:, 1] *= sum_data / sum_gras
        plt.hist(gras_data[:, 0], bins=hist_bins, weights=gras_data[:, 1], histtype='step', color='orange',
                 label=r'GRAS: p+$\alpha$+secondaries, BAM/N', density=density, linewidth=1.6, alpha=0.8)

        # gras_data = read_data(Path(path, 'my', 'hedepperpart_out_woprim_R.out'))
        # plt.hist(gras_data[:, 0], bins=hist_bins, weights=gras_data[:, 1], histtype='step', #color='green',
        #          label=r'hedepperpart_out_woprim_R.out', density=density, linewidth=1.8, alpha=1.)
        #
        # gras_data = read_data(Path(path, 'my', 'hedepperpart_out_woprim_woalphacontr_R.out'))
        # plt.hist(gras_data[:, 0], bins=hist_bins, weights=gras_data[:, 1], histtype='step', #color='green',
        #          label=r'hedepperpart_out_woprim_woalphacontr_R.out', density=density, linewidth=1.8, alpha=1.)
        #
        # gras_data = read_data(Path(path, 'my', 'hedepperparticle_out_R.out'))
        # plt.hist(gras_data[:, 0], bins=hist_bins, weights=gras_data[:, 1], histtype='step', #color='green',
        #          label=r'hedepperparticle_out_R.out', density=density, linewidth=1.8, alpha=1.)

        # gras_data = read_data(Path(path, 'my', 'hprimprotonplusinsideelec_R.out'))
        # plt.hist(gras_data[:, 0], bins=hist_bins, weights=gras_data[:, 1], histtype='step', #color='green',
        #          label=r'hprimprotonplusinsideelec_R.out', density=density, linewidth=1.8, alpha=1.)

        plt.title(title)
        plt.xlabel(r'electrons (e$^-$)')
        plt.ylabel('normalized counts')
        plt.legend(loc='upper right')
        fig.tight_layout()
        self.save_and_draw('gaia-bam-sm-gras-histograms')

    def plot_flux_spectrum(self):
        """TBW."""
        spectrum_file0 = 'data/Gaia_pGCR_201490_NEI_11mm_Al_shielding.tfx.tsv'  # MeV
        spectrum_file1 = 'data/proton_L2_solarMin1977_11mm_Shielding.txt'  # MeV
        from util import read_data
        spectrum0 = read_data(spectrum_file0)
        spectrum1 = read_data(spectrum_file1)

        spectrum_below10MeV_0 = spectrum0[np.where(spectrum0[:, 0] < 10.)]
        spectrum_cosmix_0 = spectrum0[np.where(10. <= spectrum0[:, 0])]
        spectrum_cosmix_0 = spectrum_cosmix_0[np.where(spectrum_cosmix_0[:, 0] < 1.e+4)]
        spectrum_above10GeV_0 = spectrum0[np.where(spectrum0[:, 0] >= 1.e+4)]
        spectrum_below10MeV_1 = spectrum1[np.where(spectrum1[:, 0] < 10.)]
        spectrum_cosmix_1 = spectrum1[np.where(10. <= spectrum1[:, 0])]
        spectrum_cosmix_1 = spectrum_cosmix_1[np.where(spectrum_cosmix_1[:, 0] < 1.e+4)]
        spectrum_above10GeV_1 = spectrum1[np.where(spectrum1[:, 0] >= 1.e+4)]

        import matplotlib
        font = {'size': 14}
        matplotlib.rc('font', **font)
        fig = plt.figure(figsize=(8, 4))
        plt.title('Proton flux spectrum at L2 behind 11mm Al shielding')
        plt.xlabel('Energy (MeV)')
        plt.ylabel(r'Diff. Flux (m$^{-2}$s$^{-1}$sr$^{-1}$MeV$^{-1}$)')
        plt.loglog(spectrum_cosmix_1[:, 0], spectrum_cosmix_1[:, 1], '-', linewidth=2, label='earlier: CREME 1977 SolMin')
        plt.loglog(spectrum_below10MeV_1[:, 0], spectrum_below10MeV_1[:, 1], '--', linewidth=2, color='C0')
        plt.loglog(spectrum_above10GeV_1[:, 0], spectrum_above10GeV_1[:, 1], '--', linewidth=2, color='C0')
        plt.loglog(spectrum_cosmix_0[:, 0], spectrum_cosmix_0[:, 1], '-', linewidth=2, label='current: CREME 2014/09')
        plt.loglog(spectrum_below10MeV_0[:, 0], spectrum_below10MeV_0[:, 1], '--', linewidth=2, color='C1' )
        plt.loglog(spectrum_above10GeV_0[:, 0], spectrum_above10GeV_0[:, 1], '--', linewidth=2, color='C1' )
        plt.legend()
        fig.tight_layout()
        self.save_and_draw('flux_spectrum')

    def ariel_histograms(self, edep):
        """TBW."""

        import matplotlib
        font = {'size': 14}
        matplotlib.rc('font', **font)
        fig = plt.figure(figsize=(8, 4))
        hrange = (0, 100)  # keV
        title = 'Energy deposited per event, Hg$_{0.75}$Cd$_{0.25}$Te & Silicon'
        density = True
        bins = 100

        for key, value in edep.items():
            if isinstance(value, str):
                if value.endswith('.npy'):
                    cosmix_edep = np.load(value)
                    plt.hist(cosmix_edep, bins=bins, range=hrange, density=density, linewidth=1.6,
                             histtype='step', label=r'CosmiX: p, $30\,MeV$, ' + str(key))

        plt.title(title)
        plt.xlabel('energy (keV)')
        if density:
            plt.ylabel('normalized counts')
        else:
            plt.ylabel('counts')
        plt.legend()
        fig.tight_layout()
        self.save_and_draw('ariel-mct-edep')
