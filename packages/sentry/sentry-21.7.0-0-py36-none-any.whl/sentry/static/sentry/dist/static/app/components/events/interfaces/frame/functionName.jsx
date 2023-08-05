Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var locale_1 = require("app/locale");
var FunctionName = function (_a) {
    var frame = _a.frame, showCompleteFunctionName = _a.showCompleteFunctionName, hasHiddenDetails = _a.hasHiddenDetails, className = _a.className;
    var getValueOutput = function () {
        if (hasHiddenDetails && showCompleteFunctionName && frame.rawFunction) {
            return {
                value: frame.rawFunction,
                meta: metaProxy_1.getMeta(frame, 'rawFunction'),
            };
        }
        if (frame.function) {
            return {
                value: frame.function,
                meta: metaProxy_1.getMeta(frame, 'function'),
            };
        }
        if (frame.rawFunction) {
            return {
                value: frame.rawFunction,
                meta: metaProxy_1.getMeta(frame, 'rawFunction'),
            };
        }
        return undefined;
    };
    var valueOutput = getValueOutput();
    return (<code className={className}>
      {!valueOutput ? (locale_1.t('<unknown>')) : (<annotatedText_1.default value={valueOutput.value} meta={valueOutput.meta}/>)}
    </code>);
};
exports.default = FunctionName;
//# sourceMappingURL=functionName.jsx.map