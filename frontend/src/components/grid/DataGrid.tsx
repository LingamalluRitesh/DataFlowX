import React, { useState, useMemo } from 'react';
import { ChevronDown, ChevronUp, Search, Download, Filter, ArrowUpDown } from 'lucide-react';

export interface DataGridColumn<T> {
  key: keyof T | string;
  header: string;
  render?: (item: T) => React.ReactNode;
  sortable?: boolean;
  width?: string;
}

interface DataGridProps<T> {
  data: T[];
  columns: DataGridColumn<T>[];
  pageSize?: number;
  searchPlaceholder?: string;
  searchKeys?: (keyof T | string)[];
  title?: string;
  actions?: React.ReactNode;
}

export function DataGrid<T extends Record<string, any>>({
  data,
  columns,
  pageSize = 15,
  searchPlaceholder = 'Search records...',
  searchKeys,
  title,
  actions,
}: DataGridProps<T>) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortAsc, setSortAsc] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);

  const filteredData = useMemo(() => {
    if (!searchTerm.trim()) return data;
    const lower = searchTerm.toLowerCase();
    return data.filter((item) => {
      if (searchKeys && searchKeys.length > 0) {
        return searchKeys.some((k) => String(item[k] ?? '').toLowerCase().includes(lower));
      }
      return Object.values(item).some((v) => String(v ?? '').toLowerCase().includes(lower));
    });
  }, [data, searchTerm, searchKeys]);

  const sortedData = useMemo(() => {
    if (!sortKey) return filteredData;
    return [...filteredData].sort((a, b) => {
      const valA = a[sortKey];
      const valB = b[sortKey];
      if (valA === valB) return 0;
      if (valA === null || valA === undefined) return 1;
      if (valB === null || valB === undefined) return -1;
      if (typeof valA === 'number' && typeof valB === 'number') {
        return sortAsc ? valA - valB : valB - valA;
      }
      return sortAsc
        ? String(valA).localeCompare(String(valB))
        : String(valB).localeCompare(String(valA));
    });
  }, [filteredData, sortKey, sortAsc]);

  const totalPages = Math.max(1, Math.ceil(sortedData.length / pageSize));
  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return sortedData.slice(start, start + pageSize);
  }, [sortedData, currentPage, pageSize]);

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortAsc(!sortAsc);
    } else {
      setSortKey(key);
      setSortAsc(true);
    }
  };

  const exportCSV = () => {
    if (!data.length) return;
    const headers = columns.map((c) => String(c.key)).join(',');
    const rows = sortedData.map((row) =>
      columns.map((c) => `"${String(row[c.key as keyof T] ?? '').replace(/"/g, '""')}"`).join(',')
    );
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers, ...rows].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `${title || 'export'}_data.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      {/* Header controls */}
      <div className="p-4 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-3 bg-slate-900/60">
        <div className="flex items-center gap-3">
          {title && <h3 className="font-semibold text-white text-base">{title}</h3>}
          <span className="text-xs text-slate-400 font-mono bg-slate-800 px-2 py-0.5 rounded-full">
            {filteredData.length} records
          </span>
        </div>

        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value);
                setCurrentPage(1);
              }}
              placeholder={searchPlaceholder}
              className="bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500 w-64"
            />
          </div>

          <button
            onClick={exportCSV}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-medium border border-slate-700 transition"
          >
            <Download className="w-3.5 h-3.5" />
            Export CSV
          </button>

          {actions}
        </div>
      </div>

      {/* Table grid */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-950/80 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
            <tr>
              {columns.map((col) => {
                const colKey = String(col.key);
                return (
                  <th
                    key={colKey}
                    style={{ width: col.width }}
                    onClick={() => col.sortable !== false && handleSort(colKey)}
                    className={`px-4 py-3 select-none ${
                      col.sortable !== false ? 'cursor-pointer hover:text-white' : ''
                    }`}
                  >
                    <div className="flex items-center gap-1.5">
                      <span>{col.header}</span>
                      {col.sortable !== false && (
                        <span className="text-slate-500">
                          {sortKey === colKey ? (
                            sortAsc ? (
                              <ChevronUp className="w-3.5 h-3.5 text-cyan-400" />
                            ) : (
                              <ChevronDown className="w-3.5 h-3.5 text-cyan-400" />
                            )
                          ) : (
                            <ArrowUpDown className="w-3 h-3 opacity-30" />
                          )}
                        </span>
                      )}
                    </div>
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono">
            {paginatedData.length > 0 ? (
              paginatedData.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40 transition">
                  {columns.map((col) => (
                    <td key={String(col.key)} className="px-4 py-3">
                      {col.render ? col.render(item) : String(item[col.key as keyof T] ?? '—')}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={columns.length} className="px-4 py-8 text-center text-slate-500">
                  No records matching your search query.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      {totalPages > 1 && (
        <div className="p-3 border-t border-slate-800 flex items-center justify-between bg-slate-950/60 text-xs text-slate-400">
          <div>
            Page {currentPage} of {totalPages}
          </div>
          <div className="flex items-center gap-1">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 text-slate-200"
            >
              Previous
            </button>
            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 text-slate-200"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
