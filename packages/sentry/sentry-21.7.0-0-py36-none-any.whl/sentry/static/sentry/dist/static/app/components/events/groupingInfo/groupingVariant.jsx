Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var capitalize_1 = tslib_1.__importDefault(require("lodash/capitalize"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var keyValueList_1 = tslib_1.__importDefault(require("app/components/events/interfaces/keyValueList"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var groupingComponent_1 = tslib_1.__importDefault(require("./groupingComponent"));
var utils_1 = require("./utils");
function addFingerprintInfo(data, variant) {
    if (variant.matched_rule) {
        data.push([
            locale_1.t('Fingerprint rule'),
            <TextWithQuestionTooltip key="type">
        {variant.matched_rule}
        <questionTooltip_1.default size="xs" position="top" title={locale_1.t('The server-side fingerprinting rule that produced the fingerprint.')}/>
      </TextWithQuestionTooltip>,
        ]);
    }
    if (variant.values) {
        data.push([locale_1.t('Fingerprint values'), variant.values]);
    }
    if (variant.client_values) {
        data.push([
            locale_1.t('Client fingerprint values'),
            <TextWithQuestionTooltip key="type">
        {variant.client_values}
        <questionTooltip_1.default size="xs" position="top" title={locale_1.t('The client sent a fingerprint that was overridden by a server-side fingerprinting rule.')}/>
      </TextWithQuestionTooltip>,
        ]);
    }
}
var GroupVariant = /** @class */ (function (_super) {
    tslib_1.__extends(GroupVariant, _super);
    function GroupVariant() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showNonContributing: false,
        };
        _this.handleShowNonContributing = function () {
            _this.setState({ showNonContributing: true });
        };
        _this.handleHideNonContributing = function () {
            _this.setState({ showNonContributing: false });
        };
        return _this;
    }
    GroupVariant.prototype.getVariantData = function () {
        var _a, _b;
        var _c = this.props, variant = _c.variant, showGroupingConfig = _c.showGroupingConfig;
        var data = [];
        var component;
        if (!this.state.showNonContributing && variant.hash === null) {
            return [data, component];
        }
        if (variant.hash !== null) {
            data.push([
                locale_1.t('Hash'),
                <TextWithQuestionTooltip key="hash">
          <Hash>{variant.hash}</Hash>
          <questionTooltip_1.default size="xs" position="top" title={locale_1.t('Events with the same hash are grouped together')}/>
        </TextWithQuestionTooltip>,
            ]);
        }
        if (variant.hashMismatch) {
            data.push([
                locale_1.t('Hash mismatch'),
                locale_1.t('hashing algorithm produced a hash that does not match the event'),
            ]);
        }
        switch (variant.type) {
            case types_1.EventGroupVariantType.COMPONENT:
                component = variant.component;
                data.push([
                    locale_1.t('Type'),
                    <TextWithQuestionTooltip key="type">
            {variant.type}
            <questionTooltip_1.default size="xs" position="top" title={locale_1.t('Uses a complex grouping algorithm taking event data into account')}/>
          </TextWithQuestionTooltip>,
                ]);
                if (showGroupingConfig && ((_a = variant.config) === null || _a === void 0 ? void 0 : _a.id)) {
                    data.push([locale_1.t('Grouping Config'), variant.config.id]);
                }
                break;
            case types_1.EventGroupVariantType.CUSTOM_FINGERPRINT:
                data.push([
                    locale_1.t('Type'),
                    <TextWithQuestionTooltip key="type">
            {variant.type}
            <questionTooltip_1.default size="xs" position="top" title={locale_1.t('Overrides the default grouping by a custom fingerprinting rule')}/>
          </TextWithQuestionTooltip>,
                ]);
                addFingerprintInfo(data, variant);
                break;
            case types_1.EventGroupVariantType.SALTED_COMPONENT:
                component = variant.component;
                data.push([
                    locale_1.t('Type'),
                    <TextWithQuestionTooltip key="type">
            {variant.type}
            <questionTooltip_1.default size="xs" position="top" title={locale_1.t('Uses a complex grouping algorithm taking event data and a fingerprint into account')}/>
          </TextWithQuestionTooltip>,
                ]);
                addFingerprintInfo(data, variant);
                if (showGroupingConfig && ((_b = variant.config) === null || _b === void 0 ? void 0 : _b.id)) {
                    data.push([locale_1.t('Grouping Config'), variant.config.id]);
                }
                break;
            default:
                break;
        }
        if (component) {
            data.push([
                locale_1.t('Grouping'),
                <GroupingTree key={component.id}>
          <groupingComponent_1.default component={component} showNonContributing={this.state.showNonContributing}/>
        </GroupingTree>,
            ]);
        }
        return [data, component];
    };
    GroupVariant.prototype.renderTitle = function () {
        var _a, _b, _c;
        var variant = this.props.variant;
        var isContributing = variant.hash !== null;
        var title;
        if (isContributing) {
            title = locale_1.t('Contributing variant');
        }
        else {
            var hint = (_a = variant.component) === null || _a === void 0 ? void 0 : _a.hint;
            if (hint) {
                title = locale_1.t('Non-contributing variant: %s', hint);
            }
            else {
                title = locale_1.t('Non-contributing variant');
            }
        }
        return (<tooltip_1.default title={title}>
        <VariantTitle>
          <ContributionIcon isContributing={isContributing}/>
          {locale_1.t('By')}{' '}
          {(_c = (_b = variant.description) === null || _b === void 0 ? void 0 : _b.split(' ').map(function (i) { return capitalize_1.default(i); }).join(' ')) !== null && _c !== void 0 ? _c : locale_1.t('Nothing')}
        </VariantTitle>
      </tooltip_1.default>);
    };
    GroupVariant.prototype.renderContributionToggle = function () {
        var showNonContributing = this.state.showNonContributing;
        return (<ContributingToggle merged active={showNonContributing ? 'all' : 'relevant'}>
        <button_1.default barId="relevant" size="xsmall" onClick={this.handleHideNonContributing}>
          {locale_1.t('Contributing values')}
        </button_1.default>
        <button_1.default barId="all" size="xsmall" onClick={this.handleShowNonContributing}>
          {locale_1.t('All values')}
        </button_1.default>
      </ContributingToggle>);
    };
    GroupVariant.prototype.render = function () {
        var _a = tslib_1.__read(this.getVariantData(), 2), data = _a[0], component = _a[1];
        return (<VariantWrapper>
        <Header>
          {this.renderTitle()}
          {utils_1.hasNonContributingComponent(component) && this.renderContributionToggle()}
        </Header>

        <keyValueList_1.default data={data.map(function (d) { return ({
                key: d[0],
                subject: d[0],
                value: d[1],
            }); })} isContextData isSorted={false}/>
      </VariantWrapper>);
    };
    return GroupVariant;
}(React.Component));
var VariantWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(4));
var Header = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
var VariantTitle = styled_1.default('h5')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  margin: 0;\n  display: flex;\n  align-items: center;\n"], ["\n  font-size: ", ";\n  margin: 0;\n  display: flex;\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeMedium; });
var ContributionIcon = styled_1.default(function (_a) {
    var isContributing = _a.isContributing, p = tslib_1.__rest(_a, ["isContributing"]);
    return isContributing ? (<icons_1.IconCheckmark size="sm" isCircled color="green300" {...p}/>) : (<icons_1.IconClose size="sm" isCircled color="red300" {...p}/>);
})(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var ContributingToggle = styled_1.default(buttonBar_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  justify-content: flex-end;\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space_1.default(0.5));
var GroupingTree = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var TextWithQuestionTooltip = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-template-columns: max-content min-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-template-columns: max-content min-content;\n  grid-gap: ", ";\n"])), space_1.default(0.5));
var Hash = styled_1.default('span')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    ", ";\n    width: 210px;\n  }\n"], ["\n  @media (max-width: ", ") {\n    ", ";\n    width: 210px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, overflowEllipsis_1.default);
exports.default = GroupVariant;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=groupingVariant.jsx.map