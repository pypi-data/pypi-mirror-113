Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupingConfigItem = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var groupingConfigSelect_1 = tslib_1.__importDefault(require("./groupingConfigSelect"));
var groupingVariant_1 = tslib_1.__importDefault(require("./groupingVariant"));
var EventGroupingInfo = /** @class */ (function (_super) {
    tslib_1.__extends(EventGroupingInfo, _super);
    function EventGroupingInfo() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.toggle = function () {
            _this.setState(function (state) { return ({
                isOpen: !state.isOpen,
                configOverride: state.isOpen ? null : state.configOverride,
            }); });
        };
        _this.handleConfigSelect = function (selection) {
            _this.setState({ configOverride: selection.value }, function () { return _this.reloadData(); });
        };
        return _this;
    }
    EventGroupingInfo.prototype.getEndpoints = function () {
        var _a;
        var _b = this.props, organization = _b.organization, event = _b.event, projectId = _b.projectId;
        var path = "/projects/" + organization.slug + "/" + projectId + "/events/" + event.id + "/grouping-info/";
        if ((_a = this.state) === null || _a === void 0 ? void 0 : _a.configOverride) {
            path = path + "?config=" + this.state.configOverride;
        }
        return [['groupInfo', path]];
    };
    EventGroupingInfo.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { isOpen: false, configOverride: null });
    };
    EventGroupingInfo.prototype.renderGroupInfoSummary = function () {
        var groupInfo = this.state.groupInfo;
        if (!groupInfo) {
            return null;
        }
        var groupedBy = Object.values(groupInfo)
            .filter(function (variant) { return variant.hash !== null && variant.description !== null; })
            .map(function (variant) { return variant.description; })
            .sort(function (a, b) { return a.toLowerCase().localeCompare(b.toLowerCase()); })
            .join(', ');
        return (<SummaryGroupedBy data-test-id="loaded-grouping-info">{"(" + locale_1.t('grouped by') + " " + (groupedBy || locale_1.t('nothing')) + ")"}</SummaryGroupedBy>);
    };
    EventGroupingInfo.prototype.renderGroupConfigSelect = function () {
        var configOverride = this.state.configOverride;
        var event = this.props.event;
        var configId = configOverride !== null && configOverride !== void 0 ? configOverride : event.groupingConfig.id;
        return (<GroupConfigWrapper>
        <groupingConfigSelect_1.default eventConfigId={event.groupingConfig.id} configId={configId} onSelect={this.handleConfigSelect}/>
      </GroupConfigWrapper>);
    };
    EventGroupingInfo.prototype.renderGroupInfo = function () {
        var _a = this.state, groupInfo = _a.groupInfo, loading = _a.loading;
        var showGroupingConfig = this.props.showGroupingConfig;
        var variants = groupInfo
            ? Object.values(groupInfo).sort(function (a, b) {
                var _a, _b, _c, _d;
                return a.hash && !b.hash
                    ? -1
                    : (_d = (_a = a.description) === null || _a === void 0 ? void 0 : _a.toLowerCase().localeCompare((_c = (_b = b.description) === null || _b === void 0 ? void 0 : _b.toLowerCase()) !== null && _c !== void 0 ? _c : '')) !== null && _d !== void 0 ? _d : 1;
            })
            : [];
        return (<react_1.Fragment>
        {showGroupingConfig && this.renderGroupConfigSelect()}

        {loading ? (<loadingIndicator_1.default />) : (variants.map(function (variant, index) { return (<react_1.Fragment key={variant.key}>
              <groupingVariant_1.default variant={variant} showGroupingConfig={showGroupingConfig}/>
              {index < variants.length - 1 && <VariantDivider />}
            </react_1.Fragment>); }))}
      </react_1.Fragment>);
    };
    EventGroupingInfo.prototype.renderLoading = function () {
        return this.renderBody();
    };
    EventGroupingInfo.prototype.renderBody = function () {
        var isOpen = this.state.isOpen;
        var title = (<react_1.Fragment>
        {locale_1.t('Event Grouping Information')}
        {!isOpen && this.renderGroupInfoSummary()}
      </react_1.Fragment>);
        var actions = (<ToggleButton onClick={this.toggle} priority="link">
        {isOpen ? locale_1.t('Hide Details') : locale_1.t('Show Details')}
      </ToggleButton>);
        return (<eventDataSection_1.default type="grouping-info" title={title} actions={actions}>
        {isOpen && this.renderGroupInfo()}
      </eventDataSection_1.default>);
    };
    return EventGroupingInfo;
}(asyncComponent_1.default));
var SummaryGroupedBy = styled_1.default('small')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: block;\n    margin: 0 !important;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: block;\n    margin: 0 !important;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ToggleButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-weight: 700;\n  color: ", ";\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"], ["\n  font-weight: 700;\n  color: ", ";\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; });
var GroupConfigWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  margin-top: -", ";\n"], ["\n  margin-bottom: ", ";\n  margin-top: -", ";\n"])), space_1.default(1.5), space_1.default(1));
exports.GroupingConfigItem = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n  opacity: ", ";\n  font-weight: ", ";\n  font-size: ", ";\n"], ["\n  font-family: ", ";\n  opacity: ", ";\n  font-weight: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return (p.isHidden ? 0.5 : null); }, function (p) { return (p.isActive ? 'bold' : null); }, function (p) { return p.theme.fontSizeSmall; });
var VariantDivider = styled_1.default('hr')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n  border-top: 1px solid ", ";\n"], ["\n  padding-top: ", ";\n  border-top: 1px solid ", ";\n"])), space_1.default(1), function (p) { return p.theme.border; });
exports.default = withOrganization_1.default(EventGroupingInfo);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map