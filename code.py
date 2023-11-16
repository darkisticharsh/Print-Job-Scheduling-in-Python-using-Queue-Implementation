import time
import tkinter as tk
from tkinter import ttk
import threading

class PrintJob:
    def __init__(self, job_id, pages, owner, priority=1):
        self.job_id = job_id
        self.pages = pages
        self.owner = owner
        self.priority = priority

class PrintQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, job):
        if not self.is_empty():
            index = 0
            while index < len(self.queue) and job.priority >= self.queue[index].priority:
                index += 1
            self.queue.insert(index, job)
        else:
            self.queue.append(job)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            print("Queue is empty")

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def display_status(self):
        if not self.is_empty():
            status = "Current Queue Status:\n"
            for job in self.queue:
                status += f"Job {job.job_id} - Owner: {job.owner}, Pages: {job.pages}, Priority: {job.priority}\n"
            return status
        else:
            return "Queue is empty"

class PrintQueueGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Print Queue Simulation")

        self.print_queue = PrintQueue()

        self.job_id_var = tk.IntVar()
        self.pages_var = tk.IntVar()
        self.owner_var = tk.StringVar()
        self.priority_var = tk.IntVar(value=1)

        self.create_widgets()

    def create_widgets(self):
        # Job Entry Frame
        entry_frame = ttk.Frame(self.root, padding="10")
        entry_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(entry_frame, text="Job ID:").grid(column=0, row=0, padx=5, pady=5)
        ttk.Entry(entry_frame, textvariable=self.job_id_var).grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(entry_frame, text="Pages:").grid(column=2, row=0, padx=5, pady=5)
        ttk.Entry(entry_frame, textvariable=self.pages_var).grid(column=3, row=0, padx=5, pady=5)

        ttk.Label(entry_frame, text="Owner:").grid(column=0, row=1, padx=5, pady=5)
        ttk.Entry(entry_frame, textvariable=self.owner_var).grid(column=1, row=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Priority (1-5):").grid(column=2, row=1, padx=5, pady=5)
        ttk.Entry(entry_frame, textvariable=self.priority_var).grid(column=3, row=1, padx=5, pady=5)

        ttk.Button(entry_frame, text="Submit Job", command=self.submit_job).grid(column=4, row=0, rowspan=2, padx=5, pady=5)
        ttk.Button(entry_frame, text="Process Jobs", command=self.process_jobs).grid(column=5, row=0, rowspan=2, padx=5, pady=5)

        # Status Frame
        status_frame = ttk.Frame(self.root, padding="10")
        status_frame.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.status_label = ttk.Label(status_frame, text="")
        self.status_label.grid(column=0, row=0, padx=5, pady=5)

        ttk.Button(status_frame, text="Refresh Status", command=self.refresh_status).grid(column=0, row=1, padx=5, pady=5)

   
    def process_jobs(self):
        # Process jobs in the order they are received
        if not self.print_queue.is_empty():
            current_job = self.print_queue.dequeue()
            status_text = f"Processing Job {current_job.job_id} for {current_job.owner}. Pages: {current_job.pages}, Priority: {current_job.priority}"
            self.status_label["text"] = status_text
            self.root.after(5000, self.process_jobs)  # Schedule thes

    def submit_job(self):
        try:
            job_id = self.job_id_var.get()
            pages = self.pages_var.get()
            owner = self.owner_var.get()
            priority = self.priority_var.get()

            new_job = PrintJob(job_id, pages, owner, priority)
            self.print_queue.enqueue(new_job)
            self.status_label["text"] = f"Job {new_job.job_id} added to the queue with priority {new_job.priority}."
        except Exception as e:
            self.status_label["text"] = f"Error: {e}"

    def refresh_status(self):
        status_text = self.print_queue.display_status()
        self.status_label["text"] = status_text

if __name__ == "__main__":
    root = tk.Tk()
    app = PrintQueueGUI(root)
    root.mainloop()



