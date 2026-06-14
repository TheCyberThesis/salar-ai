insert into public.departments (id, name, type, province, city, website, address) values
  ('10000000-0000-0000-0000-000000000001', 'Nearest Police Station', 'police', null, null, null, 'Use official police service channels for the relevant city/province.'),
  ('10000000-0000-0000-0000-000000000002', 'Pakistan Telecommunication Authority', 'federal_regulator', null, null, 'https://www.pta.gov.pk/', 'Verify mobile device and complaint guidance on the official PTA website.'),
  ('10000000-0000-0000-0000-000000000003', 'National Electric Power Regulatory Authority', 'federal_regulator', null, null, 'https://nepra.org.pk/', 'Verify consumer complaint guidance on the official NEPRA website.'),
  ('10000000-0000-0000-0000-000000000004', 'Oil and Gas Regulatory Authority', 'federal_regulator', null, null, 'https://ogra.org.pk/', 'Verify gas complaint guidance on the official OGRA website.'),
  ('10000000-0000-0000-0000-000000000005', 'Federal Ombudsperson Secretariat for Protection Against Harassment', 'federal_ombudsperson', null, null, 'https://www.fospah.gov.pk/', 'Verify complaint procedure and jurisdiction on the official FOSPAH website.')
on conflict (id) do nothing;

insert into public.complaint_categories (id, name, slug, description, emergency_level, department_id) values
  ('20000000-0000-0000-0000-000000000001', 'Lost Phone', 'lost_phone', 'Lost mobile phone guidance.', 'medium', '10000000-0000-0000-0000-000000000001'),
  ('20000000-0000-0000-0000-000000000002', 'Stolen Phone', 'stolen_phone', 'Stolen or snatched mobile phone guidance.', 'medium', '10000000-0000-0000-0000-000000000001'),
  ('20000000-0000-0000-0000-000000000003', 'Lost Bike', 'lost_bike', 'Lost motorcycle/bike guidance.', 'medium', '10000000-0000-0000-0000-000000000001'),
  ('20000000-0000-0000-0000-000000000004', 'Stolen Bike', 'stolen_bike', 'Stolen motorcycle/bike guidance.', 'medium', '10000000-0000-0000-0000-000000000001'),
  ('20000000-0000-0000-0000-000000000005', 'Lost Car', 'lost_car', 'Lost car guidance.', 'medium', '10000000-0000-0000-0000-000000000001'),
  ('20000000-0000-0000-0000-000000000006', 'Stolen Car', 'stolen_car', 'Stolen car guidance.', 'medium', '10000000-0000-0000-0000-000000000001'),
  ('20000000-0000-0000-0000-000000000007', 'Electricity Bill Overcharging', 'electricity_bill_overcharging', 'Electricity overbilling complaint guidance.', 'low', '10000000-0000-0000-0000-000000000003'),
  ('20000000-0000-0000-0000-000000000008', 'Gas Bill Overcharging', 'gas_bill_overcharging', 'Gas overbilling complaint guidance.', 'low', '10000000-0000-0000-0000-000000000004'),
  ('20000000-0000-0000-0000-000000000009', 'Water Bill Overcharging', 'water_bill_overcharging', 'Water overbilling complaint guidance.', 'low', null),
  ('20000000-0000-0000-0000-000000000010', 'Workplace Harassment Against Women', 'workplace_harassment_women', 'Safety-first workplace harassment complaint guidance.', 'high', '10000000-0000-0000-0000-000000000005')
on conflict (slug) do nothing;

insert into public.required_documents (category_id, document_name, required_or_optional, notes)
select c.id, d.document_name, d.required_or_optional, d.notes
from public.complaint_categories c
join (
  values
    ('lost_phone', 'CNIC copy', 'required', 'Share only with the relevant authority when required.'),
    ('lost_phone', 'IMEI number', 'optional', 'If unavailable, check phone box, receipt, Google/Apple account, PTA/DIRBS records, or telecom operator.'),
    ('lost_phone', 'Phone box or purchase receipt', 'optional', 'Useful ownership proof.'),
    ('stolen_phone', 'CNIC copy', 'required', 'Share only with the relevant authority when required.'),
    ('stolen_phone', 'IMEI number', 'optional', 'Useful for blocking/tracing-related official steps where applicable.'),
    ('stolen_phone', 'SIM/operator details', 'required', 'Needed for telecom follow-up.'),
    ('lost_bike', 'Vehicle registration book/card', 'required', 'Ownership/registration proof.'),
    ('stolen_bike', 'Vehicle registration book/card', 'required', 'Ownership/registration proof.'),
    ('lost_car', 'Vehicle registration book/card', 'required', 'Ownership/registration proof.'),
    ('stolen_car', 'Vehicle registration book/card', 'required', 'Ownership/registration proof.'),
    ('electricity_bill_overcharging', 'Current bill copy', 'required', 'Include reference/customer number.'),
    ('electricity_bill_overcharging', 'Current meter reading photo', 'required', 'Clear dated photo is helpful.'),
    ('gas_bill_overcharging', 'Current bill copy', 'required', 'Include customer/consumer number.'),
    ('gas_bill_overcharging', 'Current meter reading photo', 'required', 'Clear dated photo is helpful.'),
    ('water_bill_overcharging', 'Current bill copy', 'required', 'Local authority requirements vary.'),
    ('workplace_harassment_women', 'High-level incident summary', 'required', 'Avoid graphic details.'),
    ('workplace_harassment_women', 'Evidence or witnesses if available', 'optional', 'Preserve safely and privately.')
) as d(slug, document_name, required_or_optional, notes) on c.slug = d.slug;

insert into public.official_links (category_id, title, url, description, verified_at)
select c.id, l.title, l.url, l.description, '2026-06-14'::timestamptz
from public.complaint_categories c
join (
  values
    ('lost_phone', 'Pakistan Telecommunication Authority', 'https://www.pta.gov.pk/', 'Official PTA website for telecom/mobile device guidance verification.'),
    ('stolen_phone', 'Pakistan Telecommunication Authority', 'https://www.pta.gov.pk/', 'Official PTA website for telecom/mobile device guidance verification.'),
    ('lost_bike', 'Punjab Police', 'https://punjabpolice.gov.pk/', 'Official Punjab Police source metadata.'),
    ('stolen_bike', 'Police Khidmat Markaz Punjab', 'https://pkm.punjab.gov.pk/', 'Official Punjab Police public-service portal.'),
    ('electricity_bill_overcharging', 'NEPRA', 'https://nepra.org.pk/', 'Official electricity regulator source metadata.'),
    ('gas_bill_overcharging', 'OGRA', 'https://ogra.org.pk/', 'Official gas regulator source metadata.'),
    ('workplace_harassment_women', 'FOSPAH', 'https://www.fospah.gov.pk/', 'Official federal ombudsperson source metadata.')
) as l(slug, title, url, description) on c.slug = l.slug;

insert into public.knowledge_sources (name, authority_type, base_url, jurisdiction, is_official, notes, last_checked_at) values
  ('Pakistan Telecommunication Authority', 'federal_regulator', 'https://www.pta.gov.pk/', 'Pakistan', true, 'Official source for telecom/mobile device guidance verification.', '2026-06-14'),
  ('Islamabad Capital Police', 'police', 'https://islamabadpolice.gov.pk/', 'Islamabad', true, 'Official police source metadata.', '2026-06-14'),
  ('Police Khidmat Markaz Punjab', 'public_service_portal', 'https://pkm.punjab.gov.pk/', 'Punjab', true, 'Official Punjab public-service portal metadata.', '2026-06-14'),
  ('National Electric Power Regulatory Authority', 'federal_regulator', 'https://nepra.org.pk/', 'Pakistan', true, 'Official electricity regulator metadata.', '2026-06-14'),
  ('Oil and Gas Regulatory Authority', 'federal_regulator', 'https://ogra.org.pk/', 'Pakistan', true, 'Official gas regulator metadata.', '2026-06-14'),
  ('Federal Ombudsperson Secretariat for Protection Against Harassment', 'federal_ombudsperson', 'https://www.fospah.gov.pk/', 'Pakistan', true, 'Official workplace harassment complaint authority metadata.', '2026-06-14');

insert into public.knowledge_chunks (
  title, source_name, source_type, source_url, issuing_authority, jurisdiction, province, city,
  category, subcategory, content, summary, language, verified_at, last_checked_at, confidence_level
) values
  ('PTA mobile device and complaint guidance', 'Pakistan Telecommunication Authority', 'federal_regulator', 'https://www.pta.gov.pk/', 'Pakistan Telecommunication Authority', 'Pakistan', null, null, 'lost_or_stolen_vehicle_device', 'lost_phone', 'General Pakistan-level telecom guidance source for PTA/DIRBS/mobile device and complaint-management verification. Users should verify current blocking or complaint steps directly with PTA and telecom operators.', 'Use PTA/telecom guidance for phone IMEI/SIM-related steps after police reporting where relevant.', 'english', '2026-06-14', '2026-06-14', 'official_source_metadata'),
  ('Police loss/theft report guidance', 'Islamabad Capital Police', 'police', 'https://islamabadpolice.gov.pk/', 'Islamabad Capital Police', 'Islamabad', 'Islamabad Capital Territory', 'Islamabad', 'lost_or_stolen_vehicle_device', 'stolen_phone', 'Official police source metadata for reporting loss/theft matters in Islamabad. Exact requirements can vary by report type and should be verified with the receiving police office.', 'Police reporting source for lost/stolen devices and vehicles in Islamabad.', 'english', '2026-06-14', '2026-06-14', 'official_source_metadata'),
  ('Police Khidmat Markaz loss-report services', 'Police Khidmat Markaz Punjab', 'public_service_portal', 'https://pkm.punjab.gov.pk/', 'Punjab Police', 'Punjab', 'Punjab', null, 'lost_or_stolen_vehicle_device', 'stolen_bike', 'Official Punjab Police service portal metadata for citizen services such as loss-reporting. Exact service requirements should be verified on the official portal or service center.', 'Punjab public-service reporting source for loss reports and police service-center guidance.', 'english', '2026-06-14', '2026-06-14', 'official_source_metadata'),
  ('NEPRA consumer complaint guidance', 'National Electric Power Regulatory Authority', 'federal_regulator', 'https://nepra.org.pk/', 'NEPRA', 'Pakistan', null, null, 'utility_bill_overcharging', 'electricity_bill_overcharging', 'Official regulator source metadata for electricity consumer complaints. Users should first collect bill reference details, meter proof, provider complaint reference, and verify escalation requirements directly with NEPRA.', 'NEPRA is the federal regulator source for electricity consumer complaint escalation verification.', 'english', '2026-06-14', '2026-06-14', 'official_source_metadata'),
  ('OGRA complaint guidance', 'Oil and Gas Regulatory Authority', 'federal_regulator', 'https://ogra.org.pk/', 'OGRA', 'Pakistan', null, null, 'utility_bill_overcharging', 'gas_bill_overcharging', 'Official regulator source metadata for gas utility complaint escalation. Users should verify current OGRA complaint requirements and first collect provider complaint/reference details.', 'OGRA is the Pakistan-level regulator source for gas complaint escalation verification.', 'english', '2026-06-14', '2026-06-14', 'official_source_metadata'),
  ('FOSPAH workplace harassment complaint guidance', 'Federal Ombudsperson Secretariat for Protection Against Harassment', 'federal_ombudsperson', 'https://www.fospah.gov.pk/', 'FOSPAH', 'Pakistan', null, null, 'workplace_harassment_women', 'workplace_harassment_women', 'Official federal ombudsperson source metadata for workplace harassment guidance. Users should verify complaint procedure, jurisdiction, confidentiality, and current forms directly with FOSPAH or a relevant provincial authority.', 'FOSPAH is an official Pakistan-level source for workplace harassment complaint procedure verification.', 'english', '2026-06-14', '2026-06-14', 'official_source_metadata');
