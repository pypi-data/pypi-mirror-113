Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var DividerHandlerManager = tslib_1.__importStar(require("app/components/events/interfaces/spans/dividerHandlerManager"));
var spanGroup_1 = tslib_1.__importDefault(require("./spanGroup"));
var utils_1 = require("./utils");
var SpanTree = /** @class */ (function (_super) {
    tslib_1.__extends(SpanTree, _super);
    function SpanTree() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.traceViewRef = react_1.createRef();
        return _this;
    }
    SpanTree.prototype.renderSpan = function (_a) {
        var _this = this;
        var _b;
        var span = _a.span, childSpans = _a.childSpans, spanNumber = _a.spanNumber, treeDepth = _a.treeDepth, continuingTreeDepths = _a.continuingTreeDepths, isLast = _a.isLast, isRoot = _a.isRoot, generateBounds = _a.generateBounds;
        var spanChildren = (_b = childSpans === null || childSpans === void 0 ? void 0 : childSpans[utils_1.getSpanID(span)]) !== null && _b !== void 0 ? _b : [];
        // Mark descendents as being rendered. This is to address potential recursion issues due to malformed data.
        // For example if a span has a span_id that's identical to its parent_span_id.
        childSpans = tslib_1.__assign({}, childSpans);
        delete childSpans[utils_1.getSpanID(span)];
        var treeDepthEntry = utils_1.isOrphanDiffSpan(span)
            ? { type: 'orphan', depth: treeDepth }
            : treeDepth;
        var treeArr = isLast
            ? continuingTreeDepths
            : tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(continuingTreeDepths)), [treeDepthEntry]);
        var reduced = spanChildren.reduce(function (acc, spanChild, index) {
            var key = "" + utils_1.getSpanID(spanChild);
            var results = _this.renderSpan({
                spanNumber: acc.nextSpanNumber,
                isLast: index + 1 === spanChildren.length,
                isRoot: false,
                span: spanChild,
                childSpans: childSpans,
                continuingTreeDepths: treeArr,
                treeDepth: treeDepth + 1,
                generateBounds: generateBounds,
            });
            acc.renderedSpanChildren.push(<react_1.Fragment key={key}>{results.spanTree}</react_1.Fragment>);
            acc.nextSpanNumber = results.nextSpanNumber;
            return acc;
        }, {
            renderedSpanChildren: [],
            nextSpanNumber: spanNumber + 1,
        });
        var spanTree = (<react_1.Fragment>
        <spanGroup_1.default spanNumber={spanNumber} span={span} renderedSpanChildren={reduced.renderedSpanChildren} treeDepth={treeDepth} continuingTreeDepths={continuingTreeDepths} isRoot={isRoot} isLast={isLast} numOfSpanChildren={spanChildren.length} generateBounds={generateBounds}/>
      </react_1.Fragment>);
        return {
            nextSpanNumber: reduced.nextSpanNumber,
            spanTree: spanTree,
        };
    };
    SpanTree.prototype.renderRootSpans = function () {
        var _this = this;
        var _a = this.props, baselineEvent = _a.baselineEvent, regressionEvent = _a.regressionEvent;
        var comparisonReport = utils_1.diffTransactions({
            baselineEvent: baselineEvent,
            regressionEvent: regressionEvent,
        });
        var rootSpans = comparisonReport.rootSpans, childSpans = comparisonReport.childSpans;
        var generateBounds = utils_1.boundsGenerator(rootSpans);
        var nextSpanNumber = 1;
        var spanTree = (<react_1.Fragment key="root-spans-tree">
        {rootSpans.map(function (rootSpan, index) {
                var renderedRootSpan = _this.renderSpan({
                    isLast: index + 1 === rootSpans.length,
                    isRoot: true,
                    span: rootSpan,
                    childSpans: childSpans,
                    spanNumber: nextSpanNumber,
                    treeDepth: 0,
                    continuingTreeDepths: [],
                    generateBounds: generateBounds,
                });
                nextSpanNumber = renderedRootSpan.nextSpanNumber;
                return <react_1.Fragment key={String(index)}>{renderedRootSpan.spanTree}</react_1.Fragment>;
            })}
      </react_1.Fragment>);
        return {
            spanTree: spanTree,
            nextSpanNumber: nextSpanNumber,
        };
    };
    SpanTree.prototype.render = function () {
        var spanTree = this.renderRootSpans().spanTree;
        return (<DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
        <TraceViewContainer ref={this.traceViewRef}>{spanTree}</TraceViewContainer>
      </DividerHandlerManager.Provider>);
    };
    return SpanTree;
}(react_1.Component));
var TraceViewContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"], ["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"])));
exports.default = SpanTree;
var templateObject_1;
//# sourceMappingURL=spanTree.jsx.map