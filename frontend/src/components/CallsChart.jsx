import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const CallsChart = ({ data, isLoading, error }) => {
  if (isLoading) {
    return (
      <p className="text-center text-gray-500">
        Carregando dados do gráfico...
      </p>
    );
  }

  if (error) {
    return <p className="text-center text-red-500">{error}</p>;
  }

  if (!data || data.length === 0) {
    return (
      <p className="text-center text-gray-500">
        Não há dados suficientes para exibir o gráfico.
      </p>
    );
  }

  const formattedData = data.map((item) => ({
    hour: new Date(item.hour).toLocaleTimeString("pt-PT", {
      hour: "2-digit",
      minute: "2-digit",
    }),
    "Total de Chamadas": item.total_calls,
  }));

  return (
    <div style={{ width: "100%", height: 300 }}>
      <ResponsiveContainer>
        <LineChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="hour" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="Total de Chamadas"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CallsChart;
