# eve-multi-sell

A tiny CLI that pulls live Jita sell prices via ESI, computes CCP’s one-tick undercuts (four significant figures), and outputs a `Name<TAB>Price<TAB>Qty` list—ready to import into EVE’s multi-sell window.

Created by Nyx Aeon
---

## Installation

1. **Clone & enter the repo**
   ```bash
   git clone https://your.git.repo/eve-multi-sell.git
   cd eve-multi-sell
   ```

2. **(Optional) Create & activate a virtualenv**
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   # or on Windows PowerShell:
   .\venv\Scripts\activate
   ```

3. **Install the CLI**
   ```bash
   pip install .
   ```
   This will install all dependencies (`requests`, `pyperclip`) and register an `eve-multi-sell` command on your PATH.

---

## Usage

Follow these steps to undercut your orders in seconds:

1. **Copy** the items you want to sell from your item or corporation hangar (Ctrl + C).
2. In EVE, **right-click** on one of those items and select **Sell Items**.
3. **Run** the tool:
    - **From clipboard** (default):
      ```bash
      eve-multi-sell
      ```  
    - **From a file** (e.g. `items.txt`):
      ```bash
      eve-multi-sell items.txt
      ```  
    - **Via pipe**:
      ```bash
      cat items.txt | eve-multi-sell
      ```

4. In the top-left corner of the **Sell Items** window in EVE, click **Import Item Prices**, then **paste** (Ctrl + V).
5. **Done!** Your orders are now undercut by exactly one tick according to CCP’s four-significant-figures rule.

---

## Help & Options

```bash
eve-multi-sell --help
```

Displays usage information and available options (e.g. forcing clipboard input or specifying an input file).

---

Fly safe!
