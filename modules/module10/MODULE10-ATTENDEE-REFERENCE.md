# Module 10 reference. AI security standards and assessment evidence.

DeepCyber AI Red Teaming, AMLUCS 2026. Extended reference for the module; a one-page version is supplied separately. Source versions checked 14 September 2026.

## The documents and their roles

| Document | Status | Role |
|---|---|---|
| UK AI Cyber Security Code of Practice and Implementation Guide (DSIT, January 2025) | Published, voluntary | Baseline and implementation examples. |
| ETSI TS 104 223 (April 2025), then ETSI EN 304 223 V2.1.1 (December 2025) | Published Technical Specification, followed by a European Standard | Defines the baseline provisions: 13 principles across five lifecycle phases. Provisions use shall and should. |
| ETSI TR 104 128 V1.1.1 (May 2025); revised draft V2.0.3 (September 2026) | Published; revised draft | Explanation, threats and example measures. Clause 6.9 discusses penetration testing and red teaming. |
| ETSI TS 104 216 V0.0.8 (September 2026) | Draft | Conformance assessment specification: claims, implementation information, tailored tests and verdicts. Defining a certification scheme is outside its scope. |

The EN is voluntary as a standard. Publication does not by itself create a legal obligation, an AI Act certificate or a presumption of conformity with the AI Act.

## Two assessment terms

Implementation Conformance Statement (ICS): which provisions apply, and what the organisation claims about them. Exclusions need reasons.

Implementation eXtra Information for Testing (IXIT): the system information and evidence that support assessment of those claims, including references to existing records. The draft describes grey-box testing: the assessor uses the offered interfaces with partial design knowledge.

Verdicts: pass, fail, inconclusive. Inconclusive applies when missing or insufficient information prevents a meaningful verdict. A fail takes precedence when results are combined. A test result describes what happened; a verdict answers whether a provision was met on the full relevant evidence.

## Evidence fields for a finding

| Field | What to record |
|---|---|
| Requirement and objective | The requirement tested and the provision it bears on, with its force (shall or should). |
| Scope and version | Target, model, prompt and configuration, tool permissions, test environment, captured state. |
| Test method and criterion | The attack sequence and a separate criterion for the effect, plus a legitimate control where available. |
| Observable result | The conversation and the authenticated tool, audit or database evidence. Record any reseeding or restoration. Do not claim permanent loss without evidence. |
| Provision mapping | For the DVC deletion case: EN 5.1.2-6 (permissions), 5.2.5 (security testing), 5.4.2 (logging). Draft IXIT-AI-25 and AI-32 are related evidence categories. |
| Follow-up | Finding, affected assets, mitigation, owner, retest result, remaining limitations. |

## Where red teaming contributes to the EN

Threats and permissions (5.1.2-6; 5.1.3-1, 5.1.3-1.1). Testing before release and deployment (5.2.5-1, 5.2.5-2 shall; 5.2.5-2.1, 5.2.5-3 should). Adversarial outputs (5.2.5-4, 5.2.5-4.1 should). Logging and reassessment (5.2.4-1, 5.2.4-3; 5.4.1-2; 5.4.2-1, 5.4.2-3). The EN does not name a required tool, prescribe a campaign size or set one ASR threshold.

## Four closing questions

1. Which requirement was assessed?
2. Which system and version were covered?
3. What evidence supports the conclusion?
4. What change would require reassessment?

## Regulation, in brief

EU AI Act: Articles 9 and 15 (high-risk testing, robustness, cybersecurity); Annex IV documentation; Article 55(1)(a) adversarial testing for systemic-risk GPAI providers only. Regulation (EU) 2026/1744, Article 1(40)(b), sets the dates for Chapter III Sections 1 to 3, except Article 6(5): Article 6(2)/Annex III high-risk systems from 2 December 2027, Article 6(1)/Annex I high-risk systems from 2 August 2028. These dates do not defer the whole AI Act. DORA: Articles 24 to 26; a course test is not a TLPT. For firms within SYSC 15A.1, rule 15A.5.3R requires scenario testing; guidance 15A.5.6G includes scenarios involving corruption, deletion or manipulation of data critical to important business services. UK Cyber Security and Resilience (NIS) Bill: still a Bill. EU Cyber Resilience Act: separate product legislation; reporting from 11 September 2026, main requirements from 11 December 2027. Applicability depends on the organisation, the system and the product.

## Public sources

- [AI Cyber Security Code of Practice](https://www.gov.uk/government/publications/ai-cyber-security-code-of-practice/code-of-practice-for-the-cyber-security-of-ai) and [Implementation Guide](https://assets.publishing.service.gov.uk/media/679cae441d14e76535afb630/Implementation_Guide_for_the_AI_Cyber_Security_Code_of_Practice.pdf)
- [ETSI EN 304 223 V2.1.1](https://www.etsi.org/deliver/etsi_en/304200_304299/304223/02.01.01_60/en_304223v020101p.pdf)
- [ETSI TR 104 128 V1.1.1](https://www.etsi.org/deliver/etsi_tr/104100_104199/104128/01.01.01_60/tr_104128v010101p.pdf)
- [ETSI TS 104 216 work item](https://portal.etsi.org/webapp/WorkProgram/Report_WorkItem.asp?WKI_ID=74988) and [ETSI, Understanding standards](https://www.etsi.org/standards/understanding-standards/)
- [ETSI TR 104 065 V1.1.1](https://www.etsi.org/deliver/etsi_tr/104000_104099/104065/01.01.01_60/tr_104065v010101p.pdf), AI Act mapping
- [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) and [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng); [DORA](https://eur-lex.europa.eu/eli/reg/2022/2554/oj); [Cyber Resilience Act](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng)
- [FCA SYSC 15A.5](https://handbook.fca.org.uk/handbook/sysc15a/sysc15as5); [UK Bill 4035 stages](https://bills.parliament.uk/bills/4035/stages)
- [ICO, A guide to data security](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/security/a-guide-to-data-security/); [Bank of England CBEST](https://www.bankofengland.co.uk/financial-stability/operational-resilience-of-the-financial-sector/cbest-threat-intelligence-led-assessments-implementation-guide)
