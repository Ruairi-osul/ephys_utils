from pathlib import Path
from dotenv import load_dotenv
from ephys_queries import db_setup_core
from ephys_queries import get_raw_path
from ephys_queries import select_spike_times
from ephys_queries import select_neurons
from plot_raw import plot_raw
import matplotlib.pyplot as plt


load_dotenv()
engine, metadata = db_setup_core()
session = "hamilton_35"
base_dir = Path("/media/rory/MASSIVE1")

path = get_raw_path(engine, metadata, session_name=session)
path = base_dir / path

print("selecting neurons")
neurons = select_neurons(engine, metadata, session_names=[session])
neuron_id = neurons.id.unique()[0]
chan = int(neurons[neurons["id"]==neuron_id]["channel"].values[0])
print("selecting_spiketimes")
spiketimes = select_spike_times(engine, metadata, session_names=[session], neuron_ids=[int(neuron_id)])
spiketimes = spiketimes.spike_time_samples.divide(30000).values

print("done selecting")
ax = plot_raw(path, spiketimes, chan=chan)
print("returned ax")
plt.show()


