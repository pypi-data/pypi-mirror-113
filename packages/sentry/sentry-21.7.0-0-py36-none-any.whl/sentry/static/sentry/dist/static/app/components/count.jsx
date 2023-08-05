Object.defineProperty(exports, "__esModule", { value: true });
var formatters_1 = require("app/utils/formatters");
function Count(props) {
    var value = props.value, className = props.className;
    return (<span className={className} title={value.toLocaleString()}>
      {formatters_1.formatAbbreviatedNumber(value)}
    </span>);
}
exports.default = Count;
//# sourceMappingURL=count.jsx.map