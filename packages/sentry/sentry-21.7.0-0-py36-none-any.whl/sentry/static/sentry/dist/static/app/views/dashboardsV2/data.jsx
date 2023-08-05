Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_STATS_PERIOD = exports.INTERVAL_CHOICES = exports.DISPLAY_TYPE_CHOICES = exports.EMPTY_DASHBOARD = void 0;
var locale_1 = require("app/locale");
exports.EMPTY_DASHBOARD = {
    id: '',
    dateCreated: '',
    createdBy: undefined,
    title: locale_1.t('Untitled dashboard'),
    widgets: [],
};
exports.DISPLAY_TYPE_CHOICES = [
    { label: locale_1.t('Area Chart'), value: 'area' },
    { label: locale_1.t('Bar Chart'), value: 'bar' },
    { label: locale_1.t('Line Chart'), value: 'line' },
    { label: locale_1.t('Table'), value: 'table' },
    { label: locale_1.t('World Map'), value: 'world_map' },
    { label: locale_1.t('Big Number'), value: 'big_number' },
];
exports.INTERVAL_CHOICES = [
    { label: locale_1.t('1 Minute'), value: '1m' },
    { label: locale_1.t('5 Minutes'), value: '5m' },
    { label: locale_1.t('15 Minutes'), value: '15m' },
    { label: locale_1.t('30 Minutes'), value: '30m' },
    { label: locale_1.t('1 Hour'), value: '1h' },
    { label: locale_1.t('1 Day'), value: '1d' },
];
exports.DEFAULT_STATS_PERIOD = '24h';
//# sourceMappingURL=data.jsx.map