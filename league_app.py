import streamlit as st
import pandas as pd

# Get username and password from Streamlit Sharing environment secrets
username = st.secrets["my_username"]
password = st.secrets["my_password"]

# Login
username_input = st.sidebar.text_input("Username:")
password_input = st.sidebar.text_input("Password:", type="password")

# Check if the user is logged in
is_logged_in = (username == username_input) and (password == password_input)


# Define team names
team_names = [
    "Wuhan University of Science & Tech",
    "Wuhan University of Technology",
    "Hubei University of Technology",
    "Wuhan University",
    "Tongji University",
    "Zhonghu FC",
    "Huazhong University of Technology",
    "China University of Geosciences",
    "Wuchang University of Technology",
    "Wuhan Textile University",
    "Wuhan Institute of Technology",
    "Huazhong Agricultural University",
]

# Load existing data or create a new dataframe
try:
    df = pd.read_csv("soccer_league_table.csv")
except FileNotFoundError:
    data = {
        "Team": team_names,
        "Played": [0] * 12,
        "Wins": [0] * 12,
        "Draws": [0] * 12,
        "Losses": [0] * 12,
        "GF": [0] * 12,
        "GA": [0] * 12,
        "GD": [0] * 12,
        "Points": [0] * 12,
    }
    df = pd.DataFrame(data)

# Title
st.title("Wuhan Inter-Uni League Table")

if is_logged_in:
    # Update table values
    selected_team = st.selectbox("Select Team:", team_names)
    update_column = st.selectbox("Select Column to Update:", df.columns[1:])
    update_value = st.number_input(f"Enter New Value for {update_column}:", min_value=0)

    # Update the dataframe
    team_index = team_names.index(selected_team)
    df.at[team_index, update_column] = update_value

    # Recalculate GD and Points
    df["GD"] = df["GF"] - df["GA"]
    df["Points"] = 3 * df["Wins"] + df["Draws"]

    # Sort the dataframe by Points in descending order
    df = df.sort_values(by="Points", ascending=False).reset_index(drop=True)

    # Start numbering at 1 for logged-in users
    df.index += 1
else:
    df.index = df.index + 1 if is_logged_in else range(1, len(df) + 1)

# Display updated table or the read-only table
if is_logged_in:
    st.table(df)
else:
    st.dataframe(df.style.set_properties(**{'pointer-events': 'none'}))

# Save the updated dataframe to a file if logged in
if is_logged_in:
    df.to_csv("soccer_league_table.csv", index=False)
