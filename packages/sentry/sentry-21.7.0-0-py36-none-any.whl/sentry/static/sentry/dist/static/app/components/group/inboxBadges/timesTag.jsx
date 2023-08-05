Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var TimesTag = function (_a) {
    var lastSeen = _a.lastSeen, firstSeen = _a.firstSeen;
    return (<Wrapper>
      <StyledIconClock size="xs" color="gray300"/>
      {lastSeen &&
            getDynamicText_1.default({
                value: (<timeSince_1.default tooltipTitle={locale_1.t('Last Seen')} date={lastSeen} suffix={locale_1.t('ago')} shorten/>),
                fixed: '10s ago',
            })}
      {firstSeen && lastSeen && (<Separator className="hidden-xs hidden-sm">&nbsp;|&nbsp;</Separator>)}
      {firstSeen &&
            getDynamicText_1.default({
                value: (<timeSince_1.default tooltipTitle={locale_1.t('First Seen')} date={firstSeen} suffix={locale_1.t('old')} className="hidden-xs hidden-sm" shorten/>),
                fixed: '10s old',
            })}
    </Wrapper>);
};
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var Separator = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var StyledIconClock = styled_1.default(icons_1.IconClock)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-right: 2px;\n"], ["\n  margin-right: 2px;\n"])));
exports.default = TimesTag;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=timesTag.jsx.map