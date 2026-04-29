// apps/web/src/components/ApprovalFlow.tsx

import React from 'react';

interface ApprovalFlowProps {
  onApprove: () => void;
  onEdit: () => void;
  onReject: () => void;
  visible: boolean;
}

export const ApprovalFlow: React.FC<ApprovalFlowProps> = ({ onApprove, onEdit, onReject, visible }) => {
  if (!visible) return null;

  return (
    <div className="flex gap-2 my-3 justify-center">
      <button
        onClick={onApprove}
        className="px-5 py-2 bg-green-600 text-white rounded text-sm font-bold 
                   hover:bg-green-500 transition-colors flex items-center gap-2"
      >
        ✅ Approve Plan
      </button>
      <button
        onClick={onEdit}
        className="px-5 py-2 bg-yellow-600 text-white rounded text-sm font-bold 
                   hover:bg-yellow-500 transition-colors flex items-center gap-2"
      >
        ✏️ Edit
      </button>
      <button
        onClick={onReject}
        className="px-5 py-2 bg-red-600 text-white rounded text-sm font-bold 
                   hover:bg-red-500 transition-colors flex items-center gap-2"
      >
        ❌ Reject
      </button>
    </div>
  );
};