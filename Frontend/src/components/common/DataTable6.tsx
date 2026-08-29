import React, { useState } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '../ui/button';
import { Card } from '../ui/card';

export interface Column<T> {
  key: string;
  header: string;
  render?: (item: T) => React.ReactNode;
  sortable?: boolean;
  align?: 'left' | 'center' | 'right';
  width?: string;
}

interface DataTable6Props<T> {
  title?: string;
  description?: string;
  data: T[];
  columns: Column<T>[];
  pageSize?: number;
  keyExtractor: (item: T) => string;
  onRowClick?: (item: T) => void;
  className?: string;
  actionSlot?: React.ReactNode;
}

export function DataTable6<T>({
  title,
  description,
  data,
  columns,
  pageSize = 10,
  keyExtractor,
  onRowClick,
  className = '',
  actionSlot,
}: DataTable6Props<T>) {
  const [currentPage, setCurrentPage] = useState(1);
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');

  const handleSort = (key: string) => {
    if (sortKey === key) {
      if (sortDirection === 'asc') {
        setSortDirection('desc');
      } else {
        setSortKey(null);
        setSortDirection('asc');
      }
    } else {
      setSortKey(key);
      setSortDirection('asc');
    }
  };

  const sortedData = [...data].sort((a: any, b: any) => {
    if (!sortKey) return 0;
    const aVal = a[sortKey];
    const bVal = b[sortKey];
    if (aVal === bVal) return 0;
    if (aVal === undefined || aVal === null) return 1;
    if (bVal === undefined || bVal === null) return -1;
    if (sortDirection === 'asc') {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });

  const totalRows = sortedData.length;
  const totalPages = Math.ceil(totalRows / pageSize) || 1;
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = Math.min(startIndex + pageSize, totalRows);
  const currentRows = sortedData.slice(startIndex, endIndex);

  return (
    <div className={`space-y-3 ${className}`}>
      {(title || description || actionSlot) && (
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-1">
          <div>
            {title && (
              <h3 className="text-base font-semibold text-zinc-900 tracking-tight">
                {title}
              </h3>
            )}
            {description && (
              <p className="text-xs text-zinc-500 mt-0.5 max-w-3xl">
                {description}
              </p>
            )}
          </div>
          {actionSlot && <div>{actionSlot}</div>}
        </div>
      )}

      <div className="rounded-lg border border-zinc-200/80 bg-white overflow-x-auto shadow-xs">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-zinc-200/80 bg-zinc-50/70 text-zinc-600">
              {columns.map((col) => {
                const isCurrentSort = sortKey === col.key;
                return (
                  <th
                    key={col.key}
                    style={{ width: col.width }}
                    className={`py-3 px-4 font-semibold uppercase tracking-wider text-[11px] ${
                      col.align === 'right'
                        ? 'text-right'
                        : col.align === 'center'
                        ? 'text-center'
                        : 'text-left'
                    }`}
                  >
                    {col.sortable ? (
                      <button
                        type="button"
                        onClick={() => handleSort(col.key)}
                        className="inline-flex items-center gap-1.5 hover:text-zinc-950 transition-colors uppercase group cursor-pointer"
                      >
                        <span>{col.header}</span>
                        {isCurrentSort ? (
                          sortDirection === 'asc' ? (
                            <ArrowUp className="w-3 h-3 text-zinc-900" />
                          ) : (
                            <ArrowDown className="w-3 h-3 text-zinc-900" />
                          )
                        ) : (
                          <ArrowUpDown className="w-3 h-3 text-zinc-400 group-hover:text-zinc-600" />
                        )}
                      </button>
                    ) : (
                      <span>{col.header}</span>
                    )}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 text-zinc-800">
            {currentRows.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length}
                  className="py-8 text-center text-zinc-400 italic"
                >
                  No records found.
                </td>
              </tr>
            ) : (
              currentRows.map((item) => (
                <tr
                  key={keyExtractor(item)}
                  onClick={() => onRowClick && onRowClick(item)}
                  className={`transition-colors hover:bg-zinc-50/90 ${
                    onRowClick ? 'cursor-pointer' : ''
                  }`}
                >
                  {columns.map((col) => (
                    <td
                      key={col.key}
                      className={`py-3 px-4 ${
                        col.align === 'right'
                          ? 'text-right'
                          : col.align === 'center'
                          ? 'text-center'
                          : 'text-left'
                      }`}
                    >
                      {col.render ? col.render(item) : (item as any)[col.key]}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {totalRows > 0 && (
        <div className="flex items-center justify-between text-xs text-zinc-500 px-1 pt-1">
          <div>
            Showing {totalRows > 0 ? startIndex + 1 : 0}–{endIndex} of {totalRows} records
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="xs"
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="gap-1"
            >
              <ChevronLeft className="w-3 h-3" />
              <span>Previous</span>
            </Button>
            <span className="px-2 text-zinc-700 font-medium">
              Page {currentPage} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="xs"
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="gap-1"
            >
              <span>Next</span>
              <ChevronRight className="w-3 h-3" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

