Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var similarStackTrace_1 = tslib_1.__importDefault(require("./similarStackTrace"));
var GroupSimilarIssues = function (_a) {
    var project = _a.project, props = tslib_1.__rest(_a, ["project"]);
    return (<feature_1.default features={['similarity-view']} project={project}>
    <similarStackTrace_1.default project={project} {...props}/>
  </feature_1.default>);
};
exports.default = GroupSimilarIssues;
//# sourceMappingURL=index.jsx.map