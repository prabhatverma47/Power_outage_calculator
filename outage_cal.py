import pandas as pd
from datetime import datetime, timedelta

# Read data from log.csv
df = pd.read_csv("log.csv", names=["Date", "Start Time", "End Time"])

# Convert Start Time and End Time to datetime objects
df["Start Time"] = pd.to_datetime(df["Date"] + " " + df["Start Time"])
df["End Time"] = pd.to_datetime(df["Date"] + " " + df["End Time"])

# Calculate durations and filter based on the condition
offline_periods = []
for i in range(1, len(df)):
    previous_end = df.loc[i-1, "End Time"]
    current_start = df.loc[i, "Start Time"]
    duration = current_start - previous_end
    
    # Ignore durations less than or equal to 1 minute
    if duration > timedelta(minutes=1):
        offline_periods.append({
            "Date": df.loc[i, "Date"],
            "Start Time": df.loc[i-1, "End Time"].strftime("%H:%M:%S"),
            "End Time": df.loc[i, "Start Time"].strftime("%H:%M:%S"),
            "Duration": duration
        })

# Create DataFrame for the output
output_df = pd.DataFrame(offline_periods)

# Format duration nicely
output_df["Duration"] = output_df["Duration"].apply(lambda x: f"{int(x.total_seconds() // 3600)} hours, {int((x.total_seconds() % 3600) // 60)} minutes, {int(x.total_seconds() % 60)} seconds")

# Display and save to output.csv
print("Offline Periods:")
print(output_df)

output_df.to_csv("output.csv", index=False)
print("Output saved to output.csv")
