Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var defaultProps = {
    isLoading: false,
    isReloading: false,
    maskBackgroundColor: theme_1.default.white,
};
function LoadingContainer(props) {
    var className = props.className, children = props.children, isReloading = props.isReloading, isLoading = props.isLoading, maskBackgroundColor = props.maskBackgroundColor;
    var isLoadingOrReloading = isLoading || isReloading;
    return (<Container className={className}>
      {isLoadingOrReloading && (<div>
          <LoadingMask isReloading={isReloading} maskBackgroundColor={maskBackgroundColor}/>
          <Indicator />
        </div>)}
      {children}
    </Container>);
}
exports.default = LoadingContainer;
LoadingContainer.defaultProps = defaultProps;
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var LoadingMask = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  z-index: 1;\n  background-color: ", ";\n  width: 100%;\n  height: 100%;\n  opacity: ", ";\n"], ["\n  position: absolute;\n  z-index: 1;\n  background-color: ", ";\n  width: 100%;\n  height: 100%;\n  opacity: ", ";\n"])), function (p) { return p.maskBackgroundColor; }, function (p) { return (p.isReloading ? '0.6' : '1'); });
var Indicator = styled_1.default(loadingIndicator_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  z-index: 3;\n  width: 100%;\n"], ["\n  position: absolute;\n  z-index: 3;\n  width: 100%;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=loadingContainer.jsx.map