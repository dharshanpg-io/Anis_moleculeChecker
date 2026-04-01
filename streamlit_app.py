import streamlit as st
import io
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from rdkit.Chem import FindMolChiralCenters

# Configure the Streamlit page
st.set_page_config(page_title="Chiral Spotlight — R/S Detector", page_icon="🧬", layout="wide")

# Custom CSS for a beautiful, premium modern UI
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(14, 26, 64) 0%, rgb(9, 13, 32) 90%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sleek buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4) !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(118, 75, 162, 0.6) !important;
    }
    
    /* Text input glow */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* ID Card in Sidebar */
    .id-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0));
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        padding: 24px;
        margin-top: 10px;
        text-align: left;
        color: white;
    }
    .id-card h3 { 
        margin-bottom: 5px; 
        color: #a8b8d8; 
        font-weight: 600; 
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .id-card p { 
        margin: 8px 0; 
        font-size: 0.95rem; 
        color: #b0boca; 
    }
    .id-card .id-name { 
        font-weight: 700; 
        font-size: 1.4rem; 
        color: #ffffff; 
        letter-spacing: 0.5px;
        margin-top: 0px;
        background: -webkit-linear-gradient(45deg, #a18cd1 0%, #fbc2eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .id-card b {
        color: #e2e8f0;
        font-weight: 600;
    }
    
    /* Hide some default elements for cleaner look */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Metrics blocks */
    div[data-testid="stMetricValue"] {
        color: #a18cd1 !important;
        font-weight: 700 !important;
    }
    
</style>
""", unsafe_allow_html=True)

# Custom Main Header
st.markdown("""
<div style="text-align: center; margin-bottom: 50px; margin-top: 20px;">
    <h1 style="background: -webkit-linear-gradient(45deg, #a18cd1 0%, #fbc2eb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 4rem; font-weight: 900; margin-bottom: 0px; padding-bottom: 15px;">Chiral Spotlight</h1>
    <p style="font-size: 1.3rem; color: #a0aec0; margin-top: -15px; font-weight: 400; letter-spacing: 0.5px;">Advanced Stereochemistry & R/S Configuration Web App</p>
</div>
""", unsafe_allow_html=True)

# Student Details Sidebar
with st.sidebar:
    st.markdown("""
    <div class="id-card">
        <h3>STUDENT ID</h3>
        <p class="id-name">A ANIS FATHIMA</p>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 20px 0;">
        <p><b>Registration No:</b> RA2511026050314</p>
        <p><b>Class / Sec:</b> AIML / A</p>
        <p><b>Year / Sem:</b> I / II</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #718096; font-size: 0.85rem;'>Powered by RDKit & Streamlit</p>", unsafe_allow_html=True)

# Input section
st.markdown("### 🔬 Analyze Molecule")
smiles_input = st.text_input("Enter a SMILES string below:", value="", placeholder="e.g. C1CCC(C1)C(C)O")

# Try-out buttons
st.markdown("<span style='color: #a0aec0; font-size: 0.95rem;'>Or try an example molecule:</span>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
run_analysis = False
smiles_to_analyze = smiles_input
clicked_example = ""

with col1:
    if st.button("🌟 Erythronolide B"):
        # Erythronolide B SMILES from Chemistry.py
        smiles_to_analyze = "CC[C@@H]1[C@@H]([C@@H]([C@H](C(=O)[C@@H](C[C@@]([C@@H]([C@H]([C@@H]([C@H](C(=O)O1)C)O)C)O)(C)O)C)C)O)C"
        run_analysis = True
        clicked_example = "Erythronolide B"
with col2:
    if st.button("🌿 Artemisinin"):
        smiles_to_analyze = "CC1CCC2C(C1)C3CCC4=CC(=O)OC5C4C3(C2O5)O"
        run_analysis = True
        clicked_example = "Artemisinin"
with col3:
    if st.button("💊 Antibiotic Structure"):
        smiles_to_analyze = "CC(C)CC1C(=O)NC(C(=O)NC(C(=O)O)C(C)O)C(C)C"
        run_analysis = True
        clicked_example = "Antibiotic Structure"

# Also trigger analysis if user types and presses enter
if smiles_input and smiles_input != "":
    run_analysis = True

if run_analysis and smiles_to_analyze:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner('Performing advanced stereochemistry analysis...'):
        try:
            mol = Chem.MolFromSmiles(smiles_to_analyze)
            if mol is None:
                st.error("❌ Failed to parse molecule. Please check your SMILES string.")
            else:
                # Assign stereochemistry explicitly
                Chem.AssignStereochemistry(mol, flagPossibleStereoCenters=True, force=True)
                
                # Find chiral centers
                chiral_centers = FindMolChiralCenters(mol, includeUnassigned=True)
                
                r_count = 0
                s_count = 0
                for idx, config in chiral_centers:
                    if config == 'R':
                        r_count += 1
                    elif config == 'S':
                        s_count += 1
                
                total_chiral = len(chiral_centers)
                achiral_sp3_carbons = 0
                chiral_atoms_indices = {idx for idx, config in chiral_centers}
                
                for atom in mol.GetAtoms():
                    if atom.GetAtomicNum() == 6: # Carbon
                        if atom.GetHybridization() == Chem.HybridizationType.SP3:
                            if atom.GetIdx() not in chiral_atoms_indices:
                                achiral_sp3_carbons += 1

                # Generate 2D image coords
                AllChem.Compute2DCoords(mol)
                
                # Highlight chiral atoms
                chiral_atoms = list(chiral_atoms_indices)
                
                # Number the atoms just like in Chemistry.py
                for atom in mol.GetAtoms():
                    atom.SetProp('molAtomMapNumber', str(atom.GetIdx()))
                
                img = Draw.MolToImage(
                    mol, 
                    highlightAtoms=chiral_atoms,
                    size=(800, 800)
                )

                st.markdown("---")
                
                # Display Results Side-by-Side
                col_data, col_img = st.columns([1, 1.5])
                
                with col_data:
                    st.subheader("📊 Analysis Results" + (f" ({clicked_example})" if clicked_example else ""))
                    
                    st.metric(label="Total Chiral Centers", value=total_chiral)
                    
                    m_col1, m_col2 = st.columns(2)
                    with m_col1:
                        st.metric(label="(R) Configurations", value=r_count)
                    with m_col2:
                        st.metric(label="(S) Configurations", value=s_count)
                        
                    st.metric(label="Achiral sp³ Carbons", value=achiral_sp3_carbons)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.subheader("⚛️ Chiral Centers Details")
                    
                    if chiral_centers:
                        # Format data for Streamlit table
                        formatted_centers = [{"Atom Index": c[0], "Element": mol.GetAtomWithIdx(c[0]).GetSymbol(), "Configuration": c[1] if c[1] != '?' else 'Unassigned'} for c in chiral_centers]
                        st.table(formatted_centers)
                    else:
                        st.info("No chiral centers found in this molecule.")
                
                with col_img:
                    st.subheader("📐 Molecular Structure")
                    st.image(img, use_container_width=True, caption="Highlighted colors indicate chiral centers. Elements are numbered by atom index.")
                        
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
