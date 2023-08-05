Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var chunk_1 = tslib_1.__importDefault(require("./chunk"));
var Chunks = function (_a) {
    var chunks = _a.chunks;
    return (<ChunksSpan>
    {chunks.map(function (chunk, key) { return react_1.cloneElement(<chunk_1.default chunk={chunk}/>, { key: key }); })}
  </ChunksSpan>);
};
exports.default = Chunks;
var ChunksSpan = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  span {\n    display: inline;\n  }\n"], ["\n  span {\n    display: inline;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=chunks.jsx.map