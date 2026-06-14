create extension if not exists "pgcrypto";
create extension if not exists "vector";

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  phone text,
  city text,
  province text,
  created_at timestamptz not null default now()
);

create table if not exists public.departments (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  type text not null,
  province text,
  city text,
  website text,
  helpline text,
  address text,
  created_at timestamptz not null default now()
);

create table if not exists public.complaint_categories (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text not null unique,
  description text,
  emergency_level text not null default 'low',
  department_id uuid references public.departments(id),
  created_at timestamptz not null default now()
);

create table if not exists public.department_locations (
  id uuid primary key default gen_random_uuid(),
  department_id uuid references public.departments(id) on delete cascade,
  name text not null,
  province text,
  city text,
  area text,
  address text,
  latitude numeric,
  longitude numeric,
  google_maps_place_id text,
  created_at timestamptz not null default now()
);

create table if not exists public.required_documents (
  id uuid primary key default gen_random_uuid(),
  category_id uuid references public.complaint_categories(id) on delete cascade,
  document_name text not null,
  required_or_optional text not null default 'required',
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists public.complaint_templates (
  id uuid primary key default gen_random_uuid(),
  category_id uuid references public.complaint_categories(id) on delete cascade,
  template_text text not null,
  language text not null default 'english',
  created_at timestamptz not null default now()
);

create table if not exists public.official_links (
  id uuid primary key default gen_random_uuid(),
  category_id uuid references public.complaint_categories(id) on delete cascade,
  title text not null,
  url text not null,
  description text,
  verified_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists public.user_complaints (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  session_id uuid,
  category_id uuid references public.complaint_categories(id),
  title text not null,
  description text,
  collected_data jsonb not null default '{}'::jsonb,
  generated_report jsonb not null default '{}'::jsonb,
  status text not null default 'draft',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.chat_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  detected_language text,
  category_id uuid references public.complaint_categories(id),
  stage text not null default 'collecting_missing_info',
  collected_data jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.chat_messages (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references public.chat_sessions(id) on delete cascade,
  role text not null check (role in ('user', 'assistant', 'system')),
  content text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.feedback (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  complaint_id uuid references public.user_complaints(id) on delete set null,
  rating integer check (rating between 1 and 5),
  helpful boolean not null,
  comments text,
  created_at timestamptz not null default now()
);

create table if not exists public.knowledge_sources (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  authority_type text not null,
  base_url text,
  jurisdiction text not null,
  province text,
  city text,
  is_official boolean not null default true,
  notes text,
  last_checked_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists public.knowledge_chunks (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  source_name text not null,
  source_type text not null,
  source_url text,
  issuing_authority text not null,
  jurisdiction text not null,
  province text,
  city text,
  category text not null,
  subcategory text,
  content text not null,
  summary text,
  language text not null default 'english',
  embedding vector(768),
  verified_at timestamptz,
  last_checked_at timestamptz,
  effective_date timestamptz,
  expiry_date timestamptz,
  confidence_level text not null default 'official_source_metadata',
  created_at timestamptz not null default now()
);

create index if not exists idx_complaint_categories_slug on public.complaint_categories(slug);
create index if not exists idx_chat_sessions_user_id on public.chat_sessions(user_id);
create index if not exists idx_user_complaints_user_id on public.user_complaints(user_id);
create index if not exists idx_knowledge_chunks_category on public.knowledge_chunks(category, subcategory);
create index if not exists idx_knowledge_chunks_embedding on public.knowledge_chunks using ivfflat (embedding vector_cosine_ops) with (lists = 100);

create or replace function public.set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists set_user_complaints_updated_at on public.user_complaints;
create trigger set_user_complaints_updated_at
before update on public.user_complaints
for each row execute function public.set_updated_at();

drop trigger if exists set_chat_sessions_updated_at on public.chat_sessions;
create trigger set_chat_sessions_updated_at
before update on public.chat_sessions
for each row execute function public.set_updated_at();

alter table public.profiles enable row level security;
alter table public.user_complaints enable row level security;
alter table public.chat_sessions enable row level security;
alter table public.chat_messages enable row level security;
alter table public.feedback enable row level security;

create policy "Users can read own profile" on public.profiles
  for select using (auth.uid() = id);

create policy "Users can update own profile" on public.profiles
  for update using (auth.uid() = id);

create policy "Users can read own complaints" on public.user_complaints
  for select using (auth.uid() = user_id);

create policy "Users can create own complaints" on public.user_complaints
  for insert with check (auth.uid() = user_id or user_id is null);

create policy "Users can read own chat sessions" on public.chat_sessions
  for select using (auth.uid() = user_id);

create policy "Users can create own chat sessions" on public.chat_sessions
  for insert with check (auth.uid() = user_id or user_id is null);

create policy "Users can read messages from own sessions" on public.chat_messages
  for select using (
    exists (
      select 1 from public.chat_sessions
      where chat_sessions.id = chat_messages.session_id
      and chat_sessions.user_id = auth.uid()
    )
  );

create policy "Users can create feedback" on public.feedback
  for insert with check (auth.uid() = user_id or user_id is null);
