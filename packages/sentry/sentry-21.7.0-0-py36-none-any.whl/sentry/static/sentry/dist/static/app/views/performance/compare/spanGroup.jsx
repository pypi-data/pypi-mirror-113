Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var spanBar_1 = tslib_1.__importDefault(require("./spanBar"));
var SpanGroup = /** @class */ (function (_super) {
    tslib_1.__extends(SpanGroup, _super);
    function SpanGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showSpanTree: true,
        };
        _this.toggleSpanTree = function () {
            _this.setState(function (state) { return ({
                showSpanTree: !state.showSpanTree,
            }); });
        };
        return _this;
    }
    SpanGroup.prototype.renderSpanChildren = function () {
        if (!this.state.showSpanTree) {
            return null;
        }
        return this.props.renderedSpanChildren;
    };
    SpanGroup.prototype.render = function () {
        var _a = this.props, span = _a.span, treeDepth = _a.treeDepth, continuingTreeDepths = _a.continuingTreeDepths, spanNumber = _a.spanNumber, isLast = _a.isLast, isRoot = _a.isRoot, numOfSpanChildren = _a.numOfSpanChildren, generateBounds = _a.generateBounds;
        return (<react_1.Fragment>
        <spanBar_1.default span={span} treeDepth={treeDepth} continuingTreeDepths={continuingTreeDepths} spanNumber={spanNumber} isLast={isLast} isRoot={isRoot} numOfSpanChildren={numOfSpanChildren} showSpanTree={this.state.showSpanTree} toggleSpanTree={this.toggleSpanTree} generateBounds={generateBounds}/>
        {this.renderSpanChildren()}
      </react_1.Fragment>);
    };
    return SpanGroup;
}(react_1.Component));
exports.default = SpanGroup;
//# sourceMappingURL=spanGroup.jsx.map