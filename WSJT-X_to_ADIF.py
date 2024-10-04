import re
from datetime import datetime

# Define a template for ADIF format
ADIF_HEADER = """\
ADIF Export from WSJT-X ALL.TXT
<EOH>
"""

ADIF_QSO_TEMPLATE = """\
<CALL:{call_len}>{call}<BAND:{band_len}>{band}<FREQ:{freq_len}>{freq}<MODE:{mode_len}>{mode}<QSO_DATE:{qso_date_len}>{qso_date}<TIME_ON:{time_on_len}>{time_on}<RST_SENT:{rst_len}>{rst_sent}<RST_RCVD:{rst_len}>{rst_rcvd}<MY_GRIDSQUARE:{my_grid_len}>{my_grid}<GRIDSQUARE:{grid_len}>{grid}<EOR>
"""

# Function to extract and parse lines from ALL.TXT that are valid QSOs
def parse_wsjtx_log(file_path):
    qso_data = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

        # Pattern to match QSO lines in the ALL.TXT file
        qso_pattern = re.compile(r"([0-9\-: ]+) (.*) (\d{4}) (\d+) (.*) (\d{2})(.*)")
        
        for line in lines:
            match = qso_pattern.match(line.strip())
            if match:
                timestamp, call, freq_khz, mode, rst_sent, rst_rcvd, extra = match.groups()
                
                # Extract timestamp components
                qso_datetime = datetime.strptime(timestamp.strip(), "%Y-%m-%d %H:%M")
                qso_date = qso_datetime.strftime("%Y%m%d")
                qso_time = qso_datetime.strftime("%H%M")
                
                # Convert frequency from kHz to MHz
                freq_mhz = f"{int(freq_khz) / 1000:.3f}"
                
                # Extract other fields (simplified here; adjust as needed for ADIF spec compliance)
                grid_square = extra.strip().split()[-1] if len(extra.strip().split()) > 0 else 'UNKNOWN'
                band = "20m"  # This is an example; you could map the frequency range to an actual band
                
                qso_data.append({
                    'call': call.strip(),
                    'band': band,
                    'freq': freq_mhz,
                    'mode': mode.strip(),
                    'qso_date': qso_date,
                    'time_on': qso_time,
                    'rst_sent': rst_sent.strip(),
                    'rst_rcvd': rst_rcvd.strip(),
                    'my_grid': 'AA00aa',  # Placeholder for your grid square
                    'grid': grid_square,
                })
    
    return qso_data

# Function to write the ADIF file
def write_adif(qso_data, output_file):
    with open(output_file, 'w') as adif_file:
        adif_file.write(ADIF_HEADER)

        for qso in qso_data:
            adif_qso = ADIF_QSO_TEMPLATE.format(
                call=qso['call'], call_len=len(qso['call']),
                band=qso['band'], band_len=len(qso['band']),
                freq=qso['freq'], freq_len=len(qso['freq']),
                mode=qso['mode'], mode_len=len(qso['mode']),
                qso_date=qso['qso_date'], qso_date_len=len(qso['qso_date']),
                time_on=qso['time_on'], time_on_len=len(qso['time_on']),
                rst_sent=qso['rst_sent'], rst_rcvd=qso['rst_rcvd'], rst_len=len(qso['rst_sent']),
                my_grid=qso['my_grid'], my_grid_len=len(qso['my_grid']),
                grid=qso['grid'], grid_len=len(qso['grid']),
            )
            adif_file.write(adif_qso)

# Main logic to parse the ALL.TXT and write to ADIF
def main():
    input_file = 'ALL.TXT'  # Replace with the path to your WSJT-X ALL.TXT log file
    output_file = 'output_log.adi'  # Output ADIF file
    
    qso_data = parse_wsjtx_log(input_file)
    write_adif(qso_data, output_file)
    print(f"ADIF log written to {output_file}")

if __name__ == "__main__":
    main()
