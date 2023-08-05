Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaData_1 = tslib_1.__importDefault(require("app/components/events/meta/metaData"));
var utils_1 = require("app/utils");
/**
 * Returns the value of `object[prop]` and returns an annotated component if
 * there is meta data
 */
var Annotated = function (_a) {
    var children = _a.children, object = _a.object, objectKey = _a.objectKey, _b = _a.required, required = _b === void 0 ? false : _b;
    return (<metaData_1.default object={object} prop={objectKey} required={required}>
      {function (value, meta) {
            var toBeReturned = <annotatedText_1.default value={value} meta={meta}/>;
            return utils_1.isFunction(children) ? children(toBeReturned) : toBeReturned;
        }}
    </metaData_1.default>);
};
exports.default = Annotated;
//# sourceMappingURL=annotated.jsx.map