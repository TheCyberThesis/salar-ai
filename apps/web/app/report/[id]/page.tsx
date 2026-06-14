import { ReportPageClient } from "@/components/ReportPageClient";

export default async function ReportPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <ReportPageClient reportId={id} />
    </main>
  );
}
