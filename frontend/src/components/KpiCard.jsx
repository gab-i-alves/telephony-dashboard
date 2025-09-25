const KpiCard = ({ title, value, unit = "" }) => {
  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
        {title}
      </h3>
      <p className="mt-1 text-3xl font-semibold text-gray-900 dark:text-white">
        {value}
        {unit && <span className="text-lg font-medium">{unit}</span>}
      </p>
    </div>
  );
};

export default KpiCard;
