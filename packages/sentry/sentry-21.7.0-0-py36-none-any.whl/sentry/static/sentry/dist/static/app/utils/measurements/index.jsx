Object.defineProperty(exports, "__esModule", { value: true });
exports.formattedValue = void 0;
var formatters_1 = require("app/utils/formatters");
function formattedValue(record, value) {
    if (record && record.type === 'duration') {
        return formatters_1.getDuration(value / 1000, 3);
    }
    return value.toFixed(3);
}
exports.formattedValue = formattedValue;
//# sourceMappingURL=index.jsx.map