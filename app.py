import streamlit as st

from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

# ---------- Page setup ----------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Multi-Agent Research System")
st.caption("Search Agent → Reader Agent → Writer → Critic")

# ---------- Session state ----------
if "state" not in st.session_state:
    st.session_state.state = None
if "topic" not in st.session_state:
    st.session_state.topic = ""


def to_text(result) -> str:
    """Chains may return a str or a message object; normalise to str."""
    return result if isinstance(result, str) else getattr(result, "content", str(result))


# ---------- Sidebar ----------
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        **Pipeline steps**
        1. 🔍 Search agent finds sources
        2. 📖 Reader agent scrapes the best URL
        3. ✍️ Writer drafts the report
        4. 🧐 Critic reviews the report
        """
    )
    if st.button("🗑️ Clear results", use_container_width=True):
        st.session_state.state = None
        st.session_state.topic = ""
        st.rerun()

# ---------- Input ----------
with st.form("research_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of generative AI on railway logistics",
    )
    submitted = st.form_submit_button("🚀 Run research", use_container_width=True)

# ---------- Run pipeline ----------
if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        state = {}
        try:
            # Step 1 - search
            with st.status("Step 1 - Search agent is working...", expanded=True) as status:
                search_agent = build_search_agent()
                search_result = search_agent.invoke({
                    "messages": [(
                        "user",
                        f"Find recent, reliable and detailed information about: {topic}",
                    )]
                })
                state["search_results"] = search_result["messages"][-1].content
                st.write(state["search_results"][:500] + "...")
                status.update(label="Step 1 - Search complete ✅", state="complete", expanded=False)

            # Step 2 - reader
            with st.status("Step 2 - Reader agent is scraping top resources...", expanded=True) as status:
                reader_agent = build_reader_agent()
                reader_result = reader_agent.invoke({
                    "messages": [(
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}",
                    )]
                })
                state["scraped_content"] = reader_result["messages"][-1].content
                st.write(state["scraped_content"][:500] + "...")
                status.update(label="Step 2 - Scraping complete ✅", state="complete", expanded=False)

            # Step 3 - writer
            with st.status("Step 3 - Writer is drafting the report...", expanded=False) as status:
                research_combined = (
                    f"SEARCH RESULTS : \n {state['search_results']} \n\n"
                    f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
                )
                state["report"] = to_text(writer_chain.invoke({
                    "topic": topic,
                    "research": research_combined,
                }))
                status.update(label="Step 3 - Report drafted ✅", state="complete")

            # Step 4 - critic
            with st.status("Step 4 - Critic is reviewing the report...", expanded=False) as status:
                state["feedback"] = to_text(critic_chain.invoke({
                    "report": state["report"],
                }))
                status.update(label="Step 4 - Review complete ✅", state="complete")

            st.session_state.state = state
            st.session_state.topic = topic

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------- Results ----------
state = st.session_state.state
if state:
    st.divider()
    st.subheader(f"Results: {st.session_state.topic}")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        st.markdown(state["report"])
        st.download_button(
            "⬇️ Download report (.md)",
            data=state["report"],
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown(state["feedback"])

    with tab_search:
        st.markdown(state["search_results"])

    with tab_scraped:
        st.markdown(state["scraped_content"])