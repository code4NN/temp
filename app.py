import html
from typing import Optional, Tuple

import requests
import streamlit as st
import streamlit.components.v1 as components


def init_state() -> None:
    if "fetched_html" not in st.session_state:
        st.session_state.fetched_html = ""
    if "fetched_url" not in st.session_state:
        st.session_state.fetched_url = ""
    if "fetch_error" not in st.session_state:
        st.session_state.fetch_error = ""


def fetch_url_content(url: str) -> Tuple[Optional[str], Optional[str]]:
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text, None
    except requests.RequestException as exc:
        return None, str(exc)


def render_sidebar_controls() -> int:
    st.sidebar.header("Display Settings")
    return st.sidebar.slider("Iframe height (px)", min_value=300, max_value=2000, value=700, step=50)


def render_search_bar() -> Tuple[str, bool]:
    st.title("Simple URL Viewer")
    input_col, button_col = st.columns([5, 1])
    with input_col:
        url = st.text_input("Enter URL", placeholder="https://example.com", label_visibility="collapsed")
    with button_col:
        fetch_clicked = st.button("Fetch", use_container_width=True)
    return url.strip(), fetch_clicked


def render_iframe(content: str, height: int) -> None:
    escaped_html = html.escape(content, quote=True)
    iframe_markup = f"""
    <iframe
        srcdoc="{escaped_html}"
        style="width: 100%; border: 1px solid #ddd; border-radius: 8px;"
        height="{height}"
    ></iframe>
    """
    components.html(iframe_markup, height=height + 20, scrolling=True)


def main() -> None:
    st.set_page_config(page_title="Simple Streamlit URL Search", layout="wide")
    init_state()
    iframe_height = render_sidebar_controls()
    url, fetch_clicked = render_search_bar()

    if fetch_clicked:
        if not url:
            st.session_state.fetch_error = "Please enter a valid URL."
            st.session_state.fetched_html = ""
            st.session_state.fetched_url = ""
        else:
            content, error = fetch_url_content(url)
            if error:
                st.session_state.fetch_error = f"Could not fetch URL: {error}"
                st.session_state.fetched_html = ""
                st.session_state.fetched_url = ""
            else:
                st.session_state.fetch_error = ""
                st.session_state.fetched_html = content
                st.session_state.fetched_url = url

    if st.session_state.fetch_error:
        st.error(st.session_state.fetch_error)

    if st.session_state.fetched_html:
        # st.caption(f"Showing content from: {st.session_state.fetched_url}")
        render_iframe(st.session_state.fetched_html, iframe_height)


if __name__ == "__main__":
    main()
