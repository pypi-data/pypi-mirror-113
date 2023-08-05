Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var indicators_1 = tslib_1.__importDefault(require("app/components/indicators"));
var themeAndStyleProvider_1 = tslib_1.__importDefault(require("app/themeAndStyleProvider"));
var awsLambdaCloudformation_1 = tslib_1.__importDefault(require("./awsLambdaCloudformation"));
var awsLambdaFailureDetails_1 = tslib_1.__importDefault(require("./awsLambdaFailureDetails"));
var awsLambdaFunctionSelect_1 = tslib_1.__importDefault(require("./awsLambdaFunctionSelect"));
var awsLambdaProjectSelect_1 = tslib_1.__importDefault(require("./awsLambdaProjectSelect"));
/**
 * This component is a wrapper for specific pipeline views for integrations
 */
var pipelineMapper = {
    awsLambdaProjectSelect: [awsLambdaProjectSelect_1.default, 'AWS Lambda Select Project'],
    awsLambdaFunctionSelect: [awsLambdaFunctionSelect_1.default, 'AWS Lambda Select Lambdas'],
    awsLambdaCloudformation: [awsLambdaCloudformation_1.default, 'AWS Lambda Create Cloudformation'],
    awsLambdaFailureDetails: [awsLambdaFailureDetails_1.default, 'AWS Lambda View Failures'],
};
var PipelineView = /** @class */ (function (_super) {
    tslib_1.__extends(PipelineView, _super);
    function PipelineView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PipelineView.prototype.componentDidMount = function () {
        // update the title based on our mappings
        var title = this.mapping[1];
        document.title = title;
    };
    Object.defineProperty(PipelineView.prototype, "mapping", {
        get: function () {
            var pipelineName = this.props.pipelineName;
            var mapping = pipelineMapper[pipelineName];
            if (!mapping) {
                throw new Error("Invalid pipeline name " + pipelineName);
            }
            return mapping;
        },
        enumerable: false,
        configurable: true
    });
    PipelineView.prototype.render = function () {
        var Component = this.mapping[0];
        return (<themeAndStyleProvider_1.default>
        <indicators_1.default className="indicators-container"/>
        <Component {...this.props}/>
      </themeAndStyleProvider_1.default>);
    };
    return PipelineView;
}(React.Component));
exports.default = PipelineView;
//# sourceMappingURL=pipelineView.jsx.map