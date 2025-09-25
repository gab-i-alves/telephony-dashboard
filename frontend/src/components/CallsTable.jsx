const CallsTable = ({ calls, isLoading, error }) => {
  if (isLoading) {
    return <p className="text-center text-gray-500">A carregar chamadas...</p>;
  }

  if (error) {
    return <p className="text-center text-red-500">{error}</p>;
  }

  if (calls.length === 0) {
    return (
      <p className="text-center text-gray-500">
        Nenhuma chamada encontrada para este período.
      </p>
    );
  }

  const formatDate = (dateString) => {
    if (!dateString) return "-";
    const options = {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    };
    return new Date(dateString).toLocaleString("pt-PT", options);
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white divide-y divide-gray-200 rounded-lg shadow-md dark:bg-gray-800 dark:divide-gray-700">
        <thead className="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-gray-300">
              Início
            </th>
            <th className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-gray-300">
              Origem
            </th>
            <th className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-gray-300">
              Destino
            </th>
            <th className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-gray-300">
              Duração (s)
            </th>
            <th className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-gray-300">
              Status
            </th>
            <th className="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-gray-300">
              SIP Code
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
          {calls.map((call) => (
            <tr
              key={call.id}
              className="hover:bg-gray-100 dark:hover:bg-gray-600"
            >
              <td className="px-6 py-4 whitespace-nowrap">
                {formatDate(call.start_time)}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {call.source_number || "-"}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {call.destination_number || "-"}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">{call.duration}</td>
              <td className="px-6 py-4 whitespace-nowrap">
                {call.call_status || "-"}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {call.status_code || "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CallsTable;
