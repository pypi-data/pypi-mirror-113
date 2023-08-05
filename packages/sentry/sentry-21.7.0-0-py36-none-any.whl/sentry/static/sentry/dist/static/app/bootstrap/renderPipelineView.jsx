Object.defineProperty(exports, "__esModule", { value: true });
exports.renderPipelineView = void 0;
var tslib_1 = require("tslib");
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var constants_1 = require("app/constants");
var pipelineView_1 = tslib_1.__importDefault(require("app/views/integrationPipeline/pipelineView"));
function render(pipelineName, props) {
    var rootEl = document.getElementById(constants_1.ROOT_ELEMENT);
    react_dom_1.default.render(<pipelineView_1.default pipelineName={pipelineName} {...props}/>, rootEl);
}
function renderPipelineView() {
    var _a = window.__pipelineInitialData, name = _a.name, props = _a.props;
    render(name, props);
}
exports.renderPipelineView = renderPipelineView;
//# sourceMappingURL=renderPipelineView.jsx.map