# Implementation Plan - Fix App Rendering Issues

The goal is to fix the visual rendering issues in the "Trusted Brands" section of the Streamlit application `app.py`. Currently, the HTML content is being displayed as raw text instead of rendered elements.

## User Constraints
- OS: Windows
- Planning Mode: **Enabled**
- The "Trusted Brands" section must display logos correctly.
- The "Expert Help" button must be preserved (it is currently working).

## Proposed Changes

### 1. Refactor `app.py` - Trusted Brands Section
- The current issue is likely due to whitespace/indentation handling with `textwrap.dedent` or the presence of HTML comments interpreting as Markdown code blocks.
- **Action**: 
    - Locate the `show_dashboard` function in `app.py`.
    - Clean up the HTML string for "Trusted Partners & Brands".
    - Remove HTML comments (`<!-- ... -->`) to prevent Markdown interference.
    - Ensure correct nesting of `<div>` tags.
    - Verify `unsafe_allow_html=True` is properly passed.

### 2. Verification
- Restart the Streamlit server (or rely on auto-reload).
- Use the browser subagent to navigate to `http://localhost:8502`.
- Verify that the brands are now visible as images/logos and not text.

## Validating the Fix
- **Manual Check**: Browser subagent screenshot will show images for Govt, Bayer, John Deere, etc.
- **Automated Check**: Browser subagent will confirm no raw HTML text is visible.
