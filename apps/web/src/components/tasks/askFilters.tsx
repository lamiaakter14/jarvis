import React from 'react';

interface TaskFiltersProps {
  statuses: string[];
  selectedStatus: string;
  onFilterChange: (status: string) => void;
}

export const TaskFilters: React.FC<TaskFiltersProps> = ({
  statuses,
  selectedStatus,
  onFilterChange,
}) => {
  return (
    <div className="flex space-x-4 mb-4">
      {statuses.map((status) => (
        <button
          key={status}
          className={`btn ${selectedStatus === status ? 'btn-active' : 'btn-inactive'}`}
          onClick={() => onFilterChange(status)}
        >
          {status}
        </button>
      ))}
    </div>
  );
};