Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var body_1 = tslib_1.__importDefault(require("./body"));
var header_1 = tslib_1.__importDefault(require("./header"));
var SimilarTraceID = function (_a) {
    var _b, _c;
    var event = _a.event, props = tslib_1.__rest(_a, ["event"]);
    var traceID = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id;
    return (<Wrapper>
      <header_1.default traceID={traceID}/>
      <body_1.default traceID={traceID} event={event} {...props}/>
    </Wrapper>);
};
exports.default = SimilarTraceID;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(2));
var templateObject_1;
//# sourceMappingURL=index.jsx.map