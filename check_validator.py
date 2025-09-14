import csv
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime, timedelta

CURRENT_DATE = datetime(2025, 9, 14)
DATE_WINDOW_DAYS = 60

def validate_csv(file_path):
    errors = []
    check_numbers = {}  # Dict: check_num -> line_num for duplicates
    
    try:
        # Try opening with ASCII encoding to enforce no special chars
        with open(file_path, 'r', encoding='ascii', newline='') as csvfile:
            reader = csv.reader(csvfile)
            row_count = 0
            
            for row in reader:
                row_count += 1
                line_num = reader.line_num  # Actual file line number
                
                if not row:  # Skip empty lines
                    continue
                
                if len(row) not in (6, 7):
                    errors.append(f"Line {line_num}: Incorrect number of fields (expected 6 or 7, got {len(row)}).")
                    continue

                if len(row) == 7:
                    check_type, acct, check_num, check_date, amount, payee1, payee2 = row
                else:
                    check_type, acct, check_num, check_date, amount, payee1 = row
                    payee2 = ""  # Default empty value for optional field
                
                # Check type
                if check_type.upper() not in ('I', 'C'):
                    errors.append(f"Line {line_num}: Invalid check type '{check_type}' (must be 'I' or 'C').")
                
                # Check #
                try:
                    check_num_int = int(check_num)
                except ValueError:
                    errors.append(f"Line {line_num}: Check # '{check_num}' must be an integer.")
                    continue  # Skip duplicate check if invalid
                if check_num in check_numbers:
                    errors.append(f"Duplicate check # '{check_num}' found on lines {check_numbers[check_num]} and {line_num}.")
                else:
                    check_numbers[check_num] = line_num
                
                # Check date
                try:
                    parsed_date = datetime.strptime(check_date, '%m%d%y')
                    date_delta = abs((parsed_date - CURRENT_DATE).days)
                    if date_delta > DATE_WINDOW_DAYS:
                        errors.append(f"Line {line_num}: Date '{check_date}' is not within ±{DATE_WINDOW_DAYS} days of {CURRENT_DATE.strftime('%Y-%m-%d')} (parsed as {parsed_date.strftime('%Y-%m-%d')}).")
                except ValueError:
                    errors.append(f"Line {line_num}: Invalid date format '{check_date}' (expected mmddyy).")
                
                # Check amount
                try:
                    # Remove quotes and commas that Excel might add
                    cleaned_amount = amount.strip().strip('"\'').replace(',', '')
                    amount_float = float(cleaned_amount)
                    if amount_float <= 0:
                        errors.append(f"Line {line_num}: Amount '{amount}' must be positive.")
                except ValueError:
                    errors.append(f"Line {line_num}: Invalid amount '{amount}' (must be a number with optional decimal).")
                
                # Payee lines
                if len(payee1) > 40:
                    errors.append(f"Line {line_num}: Payee line 1 exceeds 40 characters (length {len(payee1)}).")
                if len(payee2) > 40:
                    errors.append(f"Line {line_num}: Payee line 2 exceeds 40 characters (length {len(payee2)}).")
            
            if row_count == 0:
                errors.append("File is empty—no checks found.")
    
    except UnicodeDecodeError:
        errors.append("File contains non-ASCII characters or invalid encoding (expected plain ASCII).")
    except csv.Error as e:
        errors.append(f"CSV parsing error: {str(e)}")
    except Exception as e:
        errors.append(f"Unexpected error: {str(e)}")
    
    return errors

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        errors = validate_csv(file_path)
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        if errors:
            error_text = "\n".join(errors)
            text_area.insert(tk.END, error_text)
            messagebox.showerror("Validation Errors", f"{len(errors)} errors found! See details below.")
            save_btn.pack(pady=10)  # Show save button
        else:
            text_area.insert(tk.END, "No errors found.")
            messagebox.showinfo("Success", "CSV is valid! No errors found.")
            save_btn.pack_forget()  # Hide save button
        text_area.config(state=tk.DISABLED)
        global current_errors
        current_errors = errors

def save_errors():
    if not current_errors:
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as f:
            f.write("\n".join(current_errors))
        messagebox.showinfo("Saved", "Errors saved successfully.")

# Global for errors (to save them)
current_errors = []

# GUI Setup
root = tk.Tk()
root.title("CSV Check Validator")
root.geometry("600x400")

btn = tk.Button(root, text="Select CSV File", command=select_file)
btn.pack(pady=20)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

save_btn = tk.Button(root, text="Save Errors to File", command=save_errors)
# Initially hidden; shown only if errors

root.mainloop()
