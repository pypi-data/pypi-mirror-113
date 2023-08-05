Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
function SampleRate(_a) {
    var sampleRate = _a.sampleRate;
    return <Wrapper>{sampleRate * 100 + "%"}</Wrapper>;
}
exports.default = SampleRate;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  white-space: pre-wrap;\n  word-break: break-all;\n"], ["\n  white-space: pre-wrap;\n  word-break: break-all;\n"])));
var templateObject_1;
//# sourceMappingURL=sampleRate.jsx.map