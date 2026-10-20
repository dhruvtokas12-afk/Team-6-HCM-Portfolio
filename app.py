import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Meridian Forward | Team 6", page_icon="▣", layout="wide")

st.markdown("""
<style>
.stApp{background:#F5F7F6}
section[data-testid="stSidebar"]{background:#102A43}
section[data-testid="stSidebar"] *{color:white!important}
.hero{background:linear-gradient(135deg,#102A43,#1F5C68);padding:32px 36px;border-radius:20px;color:white;margin-bottom:22px}
.hero h1{font-size:42px;margin:0 0 6px}.hero p{margin:3px 0;font-size:16px}
.kpi{background:white;border-radius:15px;padding:18px;border-left:5px solid #1FA89A;box-shadow:0 3px 14px rgba(16,42,67,.08)}
.label{font-size:11px;color:#607080;font-weight:700;text-transform:uppercase}.value{font-size:29px;color:#102A43;font-weight:800}.note{font-size:12px;color:#607080}
.ev{background:white;border:1px solid #DCE5E8;border-radius:14px;padding:17px;min-height:145px}
.case{color:#14786E}.calc{color:#245273}.assume{color:#8A5A00}.gate{color:#5D438A}
</style>
""", unsafe_allow_html=True)

role_gaps=pd.DataFrame({"Role":["Data Preparation","Quality Assurance","Legacy Systems","Operations","Engineering / Analytics"],"Hours":[328,84,80,8,-144]})
residual=pd.DataFrame({"Role":["Data Preparation","Quality Assurance","Legacy Systems"],"Residual Gap":[68,60,52],"Vendor Cost":[96000,136000,176000]})

st.sidebar.markdown("## TEAM 6")
st.sidebar.markdown("### MERIDIAN FORWARD")
page=st.sidebar.radio("Navigate",["Problem","Solution"])
st.sidebar.caption("HCM AS2 · Evidence Portfolio")

st.markdown("""<div class="hero"><h1>Meridian Forward</h1><p>Team 6 · HCM AS2 Evidence Portfolio</p><p>From problem → evidence → assumptions → solution</p></div>""",unsafe_allow_html=True)

if page=="Problem":
    st.markdown("## 01 · PROBLEM")
    st.markdown("### How do we give the new work the people, roles and capacity it needs — without weakening legacy service?")
    cols=st.columns(4)
    data=[("Pilot demand","2,320 h","Four-week pilot"),("Usable supply","1,964 h","Internal capacity"),("Net deficit","356 h","Demand − usable supply"),("Gross role gaps","500 h","Before spare capacity elsewhere")]
    for c,(l,v,n) in zip(cols,data):
        with c: st.markdown(f'<div class="kpi"><div class="label">{l}</div><div class="value">{v}</div><div class="note">{n}</div></div>',unsafe_allow_html=True)

    a,b=st.columns([1.1,1])
    with a:
        cap=pd.DataFrame({"Measure":["Pilot demand","Usable internal supply"],"Hours":[2320,1964]})
        fig=px.bar(cap,x="Measure",y="Hours",text="Hours",title="Four-week pilot: demand vs usable supply")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=390,showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
    with b:
        st.markdown("#### What the evidence says")
        st.markdown("**356 hours** is the net deficit after comparing total pilot demand with usable internal supply.")
        st.markdown("The **500-hour gross role gap** is a role-level view before considering the **144 hours of spare capacity elsewhere**.")
        st.info("We do not assume spare hours are transferable without a role/skill match.")

    rg=role_gaps.copy(); rg["Display"]=rg["Hours"].abs()
    fig=px.bar(rg,x="Display",y="Role",orientation="h",text="Hours",title="Role-level gaps / spare capacity")
    fig.update_traces(texttemplate="%{text} h",textposition="outside")
    fig.update_layout(height=410,xaxis_title="Hours",yaxis_title="")
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("### Evidence and assumptions")
    x,y,z=st.columns(3)
    with x: st.markdown('<div class="ev"><b class="case">CASE / WORKBOOK EVIDENCE</b><h4>Pilot capacity</h4><p>Demand = 2,320 h; usable internal supply = 1,964 h.</p></div>',unsafe_allow_html=True)
    with y: st.markdown('<div class="ev"><b class="calc">CALCULATION</b><h4>Net deficit</h4><p>2,320 − 1,964 = <b>356 h</b>.</p></div>',unsafe_allow_html=True)
    with z: st.markdown('<div class="ev"><b class="assume">TEAM ASSUMPTION</b><h4>Transferability</h4><p>144 spare hours elsewhere are not counted against specialist gaps unless a skill match is demonstrated.</p></div>',unsafe_allow_html=True)

    st.markdown("### Other constraints")
    st.markdown("- The **600-position request is not treated as four-week pilot staffing**.")
    st.markdown("- Permanent-hire lead time is separated from immediate pilot readiness.")
    st.markdown("- **Selected ≠ ready**: deployability requires readiness gates.")
    st.markdown("- Legacy service continuity remains protected.")

else:
    st.markdown("## 02 · SOLUTION")
    st.markdown("### Recruit only for the residual gap — then clear the gates that turn a person into deployable capacity.")
    cols=st.columns(3)
    data=[("Residual gap","180 h","68 + 60 + 52"),("Pilot vendor roles","3","Targeted specialist gaps"),("Conditional cost","₹4.08 lakh","96k + 136k + 176k")]
    for c,(l,v,n) in zip(cols,data):
        with c: st.markdown(f'<div class="kpi"><div class="label">{l}</div><div class="value">{v}</div><div class="note">{n}</div></div>',unsafe_allow_html=True)

    a,b=st.columns(2)
    with a:
        fig=px.bar(residual,x="Role",y="Residual Gap",text="Residual Gap",title="Residual role gaps")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=390)
        st.plotly_chart(fig,use_container_width=True)
    with b:
        fig=px.bar(residual,x="Role",y="Vendor Cost",text="Vendor Cost",title="Indicative vendor cost by role")
        fig.update_traces(texttemplate="₹%{y:,.0f}",textposition="outside")
        fig.update_layout(height=390,yaxis_title="₹")
        st.plotly_chart(fig,use_container_width=True)

    st.markdown("### Selection → readiness")
    funnel=go.Figure(go.Funnel(y=["Identified gap","Targeted sourcing","Selection evidence","Ready for deployment"],x=[180,180,180,180],textinfo="label"))
    funnel.update_layout(height=350,title="Deployability is a gated process")
    st.plotly_chart(funnel,use_container_width=True)

    g1,g2,g3=st.columns(3)
    for c,title,body in [
        (g1,"ACCESS","Authorised systems, information and permissions are available."),
        (g2,"COVER","Legacy service remains protected."),
        (g3,"AUTHORITY","Supervision and decision limits are clear.")]:
        with c: st.markdown(f'<div class="ev"><b class="gate">READY GATE</b><h4>{title}</h4><p>{body}</p></div>',unsafe_allow_html=True)

    st.markdown("### Assumption register")
    assumptions=pd.DataFrame([
        ["A1","Spare capacity","144 h elsewhere is not transferable without a role/skill match.","Team assumption"],
        ["A2","Sourcing","Internal mobility is attempted before external vendor sourcing.","Team proposal"],
        ["A3","Readiness","Selection alone is not treated as productive capacity.","Team proposal"],
        ["A4","600 positions","Longer-term request is separate from four-week pilot staffing.","Interpretation"],
        ["A5","Decision rights","High-risk / reserved decisions remain with existing owners.","Team proposal"],
    ],columns=["ID","Topic","Assumption","Type"])
    st.dataframe(assumptions,use_container_width=True,hide_index=True)

    st.success("Decision: use targeted external support only for the residual specialist gaps, while protecting legacy service and keeping decision rights bounded.")

    st.markdown("### Evidence trail")
    st.markdown("**Evidence:** workbook calculations → **Calculation:** gap/cost build-up → **Assumption:** transferability/readiness → **Decision:** targeted sourcing.")

st.markdown("<div style='text-align:center;color:#708090;padding:24px;font-size:12px'>TEAM 6 · MERIDIAN FORWARD · HCM AS2</div>",unsafe_allow_html=True)
