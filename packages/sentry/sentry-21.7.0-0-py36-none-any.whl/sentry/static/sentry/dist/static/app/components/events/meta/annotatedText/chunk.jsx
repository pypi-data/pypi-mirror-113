Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var redaction_1 = tslib_1.__importDefault(require("./redaction"));
var utils_1 = require("./utils");
var Chunk = function (_a) {
    var chunk = _a.chunk;
    if (chunk.type === 'redaction') {
        var title = utils_1.getTooltipText({ rule_id: chunk.rule_id, remark: chunk.remark });
        return (<tooltip_1.default title={title}>
        <redaction_1.default>{chunk.text}</redaction_1.default>
      </tooltip_1.default>);
    }
    return <span>{chunk.text}</span>;
};
exports.default = Chunk;
//# sourceMappingURL=chunk.jsx.map