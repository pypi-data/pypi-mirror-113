Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var utils_1 = require("app/utils");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
function FileSize(props) {
    var className = props.className, bytes = props.bytes;
    return (<span className={className}>
      {getDynamicText_1.default({ value: utils_1.formatBytesBase2(bytes), fixed: 'xx KB' })}
    </span>);
}
exports.default = FileSize;
//# sourceMappingURL=fileSize.jsx.map