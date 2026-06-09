"use client";

import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { ExternalLink, Landmark, Star } from "lucide-react";
import { api } from "@/lib/api";
import { useAppStore } from "@/lib/store";
import { formatCurrency } from "@/lib/utils";

export default function SchemeDiscovery() {
  const { userId } = useAppStore();

  const { data: schemes, isLoading } = useQuery({
    queryKey: ["schemes", userId],
    queryFn: () => api.getSchemes(userId!),
    enabled: !!userId,
  });

  if (!userId) {
    return (
      <div className="flex h-full items-center justify-center text-slate-400">
        Select a persona to discover eligible schemes
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center text-slate-400">
        Scanning 70+ government schemes...
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto p-6" role="region" aria-label="Government scheme discovery">
      <div className="mb-6">
        <h2 className="text-xl font-bold gradient-text">Scheme Discovery Agent</h2>
        <p className="text-sm text-slate-400">
          {schemes?.length || 0} schemes matched to your Digital Twin profile
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {schemes?.map((scheme, i) => (
          <motion.div
            key={scheme.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className="glass rounded-2xl p-5 transition-all hover:border-emerald-500/30"
          >
            <div className="mb-3 flex items-start justify-between">
              <div className="flex items-center gap-2">
                <div className="rounded-lg bg-amber-500/10 p-2">
                  <Landmark size={18} className="text-amber-400" />
                </div>
                <div>
                  <h3 className="font-semibold">{scheme.name}</h3>
                  <p className="text-xs text-emerald-400">{scheme.benefit_amount}</p>
                </div>
              </div>
              <div className="flex items-center gap-0.5 text-amber-400">
                {Array.from({ length: 5 - scheme.difficulty }).map((_, j) => (
                  <Star key={j} size={10} fill="currentColor" />
                ))}
              </div>
            </div>

            <p className="mb-3 text-xs text-slate-400">{scheme.eligibility}</p>
            <p className="mb-3 text-sm font-medium text-emerald-400">
              Est. value: {formatCurrency(scheme.estimated_value)}
            </p>

            <ol className="mb-4 space-y-1">
              {scheme.steps.map((step, j) => (
                <li key={j} className="flex gap-2 text-xs text-slate-400">
                  <span className="text-emerald-500">{j + 1}.</span>
                  {step}
                </li>
              ))}
            </ol>

            <a
              href={scheme.application_link}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 rounded-lg bg-emerald-500/10 px-3 py-1.5 text-xs text-emerald-400 hover:bg-emerald-500/20"
              aria-label={`Apply for ${scheme.name}`}
            >
              Apply Now <ExternalLink size={12} />
            </a>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
