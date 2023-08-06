import numpy as np
import pandas as pd
import seaborn_extensions

df = pd.DataFrame()
a = np.asarray([1, 2, 3])

seaborn_extensions.volcano_plot(1)
seaborn_extensions.volcano_plot(a)
seaborn_extensions.volcano_plot(df)
