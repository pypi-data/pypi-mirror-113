Object.defineProperty(exports, "__esModule", { value: true });
exports.MonitorsContainer = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var organization_1 = require("app/styles/organization");
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var Body = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  flex-direction: column;\n  flex: 1;\n"], ["\n  background-color: ", ";\n  flex-direction: column;\n  flex: 1;\n"])), function (p) { return p.theme.backgroundSecondary; });
var MonitorsContainer = function (_a) {
    var children = _a.children;
    return (<feature_1.default features={['monitors']} renderDisabled>
    <globalSelectionHeader_1.default showEnvironmentSelector={false} showDateSelector={false} resetParamsOnChange={['cursor']}>
      <organization_1.PageContent>
        <Body>{children}</Body>
      </organization_1.PageContent>
    </globalSelectionHeader_1.default>
  </feature_1.default>);
};
exports.MonitorsContainer = MonitorsContainer;
exports.default = withGlobalSelection_1.default(MonitorsContainer);
var templateObject_1;
//# sourceMappingURL=index.jsx.map