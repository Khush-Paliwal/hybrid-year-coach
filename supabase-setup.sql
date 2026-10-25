-- Hybrid Year Coach: one table holds every log document (settings, tests, milestones, one row per day).
-- Paste into Supabase: SQL Editor -> New query -> Run.

create table if not exists public.docs (
  user_id    uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  path       text        not null,
  data       jsonb       not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, path)
);

-- Row-level security: a signed-in person can only ever see and change their own rows.
alter table public.docs enable row level security;

drop policy if exists "read own docs" on public.docs;
drop policy if exists "add own docs" on public.docs;
drop policy if exists "change own docs" on public.docs;
drop policy if exists "remove own docs" on public.docs;

create policy "read own docs"   on public.docs for select to authenticated using ((select auth.uid()) = user_id);
create policy "add own docs"    on public.docs for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "change own docs" on public.docs for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "remove own docs" on public.docs for delete to authenticated using ((select auth.uid()) = user_id);
