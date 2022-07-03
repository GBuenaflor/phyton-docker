import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from apps import commonmodules
import dash_bootstrap_components as dbc
from app import app
from dash.exceptions import PreventUpdate

layout = html.Div(children=[
    html.A("Return to log-in page", href='/login', style={"textDecoration": "underline", "cursor": "pointer", "textAlign":"left"}),
    html.H1("UNIVERSITY OF THE PHILIPPINES DILIMAN PRIVACY POLICY",
            className="text-center", style={'marginTop': '40px'}),
    html.Hr(),
    dcc.Markdown('''
    The University of the Philippines Diliman needs to process your personal and sensitive personal information—that is, information that identifies you as an individual.
    UP is committed to comply with the Philippine Data Privacy Act of 2012 (DPA) in order to protect your right to data privacy.
    This notice explains in general terms the purpose and legal basis for the processing of the typical or usual examples of personal and sensitive personal information that UP collects from employees like you, the measures in place to protect your data privacy and the rights that you may exercise in relation to such information. Please note that this document does not contain an exhaustive list of all of UP's processing systems as well as the purpose and legal basis for processing.
    Under the DPA, personal information may be processed (e.g. collected, used, stored, disclosed, etc.) with the consent of the data subject, pursuant to a contract with the data subject; when it is necessary in order for UP to comply with a legal obligation; to protect your vitally important interests including life and health; respond to a national emergency, public order, and safety; fulfill the functions of public authority or pursuant to the legitimate interests of the University or a third party; except where such interests are overridden by your fundamental rights.
    Sensitive personal information (e.g. confidential educational records, age/birthdate, civil status, health, religious affiliation etc.) on the other hand may be processed with the consent of the data subject, when such is allowed by laws and regulations, such regulatory enactments provide for the protection of such information, and the consent of the data subject is not required for such law or regulation. For example, under the Education Act of 1982, parents have the right to access the educational records of children who are under their parental responsibility. Processing may also be done when needed to protect the life and health of the data subject or another person, and the data subject is unable to legally or physically express consent; in the case of medical treatment; or needed for the protection of lawful rights and interests of natural or legal persons in court proceedings; and for the establishment, exercise or defense of legal claims; or where provided to government or public authority.
    The term UP/University/us refers to the University of the Philippines System and Constituent University (CU) offices.
    The term you/your refers to all employees of the University of the Philippines System, as well as those seeking to be employed or have been separated from the University. 




    '''),

    html.H3("UNIVERSITY OF THE PHILIPPINES DILIMAN PRIVACY POLICY FOR FACULTY",
            className="text-center", style={'marginTop': '40px'}),

    html.Label(["In recognition of the constitutional and inherent right of people to privacy, the University of the Philippines Diliman (“UP Diliman”) advances its commitment to protect and uphold the privacy of personal information through this **UP Diliman Privacy Policy for Faculty**. This Policy is a derivative of and subject to the UP Diliman Privacy Policy at ", html.A(
        'https://upd.edu.ph/privacy/', style={'text-transform': 'lowercase'}, href='https://upd.edu.ph/privacy/')]),


    dcc.Markdown('''
    ** I.       Who are covered by this Policy**

    This Policy governs UP Diliman **Faculty, including visiting faculty (“Faculty”)** whose personal information, sensitive personal information and privileged information (“Personal Data”) are processed by UP Diliman.


    ** II.       Why are Personal Data processed?**

    UP Diliman processes Personal Data to –

    * (1) Perform its obligations, exercise its rights, and conduct its associated functions as:
        * an instrumentality of the government;
        * a higher education institution and the national university;
        * a juridical entity with its own rights, interests and internal and external affairs.
    * (2) For each particular unit of UP Diliman, conduct all acts reasonably foreseeable from and customarily performed by similar bodies.


    ** III.       What Personal Data are processed?**

    UP Diliman processes Personal Data of Faculty including but not limited to:

    * Personal details such as name, birth, gender, civil status and affiliations;
    * Contact information such as address, email, mobile and telephone numbers;
    * Academic information such as grades, course and academic standing;
    * Employment information such as government-issued numbers, position and functions;
    * Medical information such as physical, psychiatric and psychological information.

    UP Diliman processes other Personal Data of Faculty necessary for the following purposes (the “Purposes”):

    * (1) Administration of human resources such as:
        * Processing and provision of employee rights;
        * Provision of compensation and benefits;
    * (2) Administration, management and supervision of faculty in academic and non- academic functions such as:
        * Assignment of teaching load and functions, evaluation of performance, and promotion or transfer;
        * Research, ethics and intellectual property matters;
    * (3) Records and account creation, update and maintenance purposes;
    * (4) Security and community affairs purposes; and
    * (5) Purposes necessary for UP Diliman to perform its obligations, exercise its rights, and conduct its associated functions as a higher education institution, an instrumentality of the government, and as a juridical entity with its own rights, interests and internal and external affairs.

    ** IV.       How does UP Diliman process Personal Data and how long are Personal Data retained?**

    UP Diliman processes and retains Personal Data as necessary for the Purposes in accordance with:

    * (1) The Data Privacy Act of 2012, National Archives of the Philippines Act of 2007 and their Implementing Rules and Regulations;
    * (2) Policies, guidelines, and rules of the UP System and UP Diliman on data privacy, research and ethical codes of conduct; and
    * (3) Executive and regulatory issuances such as those on Freedom of Information.

    ** V.       Where are Personal Data stored and how are these transmitted?**

    Personal Data are stored in physical and electronic “Data Processing Systems” of UP Diliman as defined under National Privacy Commission Circular No. 17-01. Personal Data are transmitted in accordance with Chapter III of the Data Privacy Act of 2012 and Rule V of its Implementing Rules and Regulations.

    ** VI.       What are the rights and responsibilities of Faculty?**

    The rights and responsibilities of Faculty are governed by the **UP Diliman Data Subject Rights and Responsibilities** at https://upd.edu.ph/privacy/rightsandresponsibliities

    ** VII.       Effectivity and Definition of Terms**

    The effectivity of this policy and the definition of terms used here are those used in the **UP Diliman Privacy Policy** at https://upd.edu.ph/privacy/dilimanprivacy

    ** VIII. The Data Protection Officer**

    For data protection concerns or to report privacy incidents, please contact the UP Diliman Data Protection Officer by visiting https://upd.edu.ph/privacy

    '''),
    html.Br(),
    html.Br(),
    html.P("—————", className="text-center"),
    html.Br(),
    html.Br(),
    html.H3("UNIVERSITY OF THE PHILIPPINES DILIMAN PRIVACY POLICY FOR STAFF", className="text-center"),
    html.Hr(),

    dcc.Markdown('''

    This Policy is a derivative of and subject to the UP Diliman Privacy Policy at https://upd.edu.ph/privacy/dilimanprivacy

    ** I.       Who are covered by this Policy**

    This Policy governs UP Diliman Staff, including Research, Extension and Professional **Staff (REPS), UP contractual personnel, Non-UP contractual personnel, and retirees (“Staff”)** whose personal information, sensitive personal information and privileged information (“Personal Data”) are processed by UP Diliman.


    ** II.       Why are Personal Data processed?**

    UP Diliman processes Personal Data to –

    * (1) Perform its obligations, exercise its rights, and conduct its associated functions as:
        * an instrumentality of the government;
        * a higher education institution and the national university;
        * a juridical entity with its own rights, interests and internal and external affairs.
    * (2) For each particular unit of UP Diliman, conduct all acts reasonably foreseeable from and customarily performed by similar bodies.


    ** III.       What Personal Data are processed?**

    UP Diliman processes Personal Data of Faculty including but not limited to:

    * Personal details such as name, birth, gender, civil status and affiliations;
    * Contact information such as address, email, mobile and telephone numbers;
    * Academic information such as grades, course and academic standing;
    * Employment information such as government-issued numbers, position and functions;
    * Applicant information such as academic background and previous employments;
    * Medical information such as physical, psychiatric and psychological information.

    UP Diliman processes other Personal Data of Faculty necessary for the following purposes (the “Purposes”):

    * (1) Administration of human resources such as:
        * Processing and provision of employee rights;
        * Provision of compensation and benefits;
    * (2) Management and supervision of employees and work conduct such as:
        * Employee administration, assignment, work supervision, evaluation, promotion, discipline, and transfer;
        * Preservation of labor relations and industrial peace;
    * (3) Records and account creation, update and maintenance purposes;
    * (4) Security and community affairs purposes; and
    * (5) Purposes necessary for UP Diliman to perform its obligations, exercise its rights, and conduct its associated functions as a higher education institution, an instrumentality of the government, and as a juridical entity with its own rights, interests and internal and external affairs.

    ** IV.       How does UP Diliman process Personal Data and how long are Personal Data retained?**

    UP Diliman processes and retains Personal Data as necessary for the Purposes in accordance with:

    * (1) The Data Privacy Act of 2012, National Archives of the Philippines Act of 2007 and their Implementing Rules and Regulations;
    * (2) Policies, guidelines, and rules of the UP System and UP Diliman on data privacy, research and ethical codes of conduct; and
    * (3) Executive and regulatory issuances such as those on Freedom of Information.

    ** V.       Where are Personal Data stored and how are these transmitted?**

    Personal Data are stored in physical and electronic “Data Processing Systems” of UP Diliman as defined under National Privacy Commission Circular No. 17-01. Personal Data are transmitted in accordance with Chapter III of the Data Privacy Act of 2012 and Rule V of its Implementing Rules and Regulations.

    ** VI.       What are the rights and responsibilities of Faculty?**

    The rights and responsibilities of Faculty are governed by the **UP Diliman Data Subject Rights and Responsibilities** at https://upd.edu.ph/privacy/rightsandresponsibliities

    ** VII.       Effectivity and Definition of Terms**

    The effectivity of this policy and the definition of terms used here are those used in the **UP Diliman Privacy Policy** at https://upd.edu.ph/privacy/dilimanprivacy

    ** VIII. The Data Protection Officer**

    For data protection concerns or to report privacy incidents, please contact the UP Diliman Data Protection Officer by visiting https://upd.edu.ph/privacy

    '''),

    html.P("—————", className="text-center"),
    html.Label(["Policies seen above and more information can be found by clicking ", html.A('here', style={
               'text-transform': 'lowercase'}, href='https://upd.edu.ph/privacy/')], style={'marginLeft': '175px'}, className="text-center")
], style={'marginLeft': '0px', 'marginRight': '245px'})
