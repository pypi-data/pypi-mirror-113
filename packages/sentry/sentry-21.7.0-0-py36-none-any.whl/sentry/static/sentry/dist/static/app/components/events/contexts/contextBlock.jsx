Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var ContextBlock = function (_a) {
    var data = _a.data, _b = _a.raw, raw = _b === void 0 ? false : _b;
    if (data.length === 0) {
        return null;
    }
    return (<errorBoundary_1.default mini>
      <keyValueList_1.default data={data} raw={raw} isContextData/>
    </errorBoundary_1.default>);
};
exports.default = ContextBlock;
//# sourceMappingURL=contextBlock.jsx.map