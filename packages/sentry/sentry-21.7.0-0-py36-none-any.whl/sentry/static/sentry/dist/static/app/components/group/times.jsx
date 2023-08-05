Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Times = function (_a) {
    var lastSeen = _a.lastSeen, firstSeen = _a.firstSeen;
    return (<Container>
    <FlexWrapper>
      {lastSeen && (<react_1.Fragment>
          <StyledIconClock size="11px"/>
          <timeSince_1.default date={lastSeen} suffix={locale_1.t('ago')}/>
        </react_1.Fragment>)}
      {firstSeen && lastSeen && (<span className="hidden-xs hidden-sm">&nbsp;—&nbsp;</span>)}
      {firstSeen && (<timeSince_1.default date={firstSeen} suffix={locale_1.t('old')} className="hidden-xs hidden-sm"/>)}
    </FlexWrapper>
  </Container>);
};
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 1;\n  min-width: 0; /* flex-hack for overflow-ellipsised children */\n"], ["\n  flex-shrink: 1;\n  min-width: 0; /* flex-hack for overflow-ellipsised children */\n"])));
var FlexWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n\n  /* The following aligns the icon with the text, fixes bug in Firefox */\n  display: flex;\n  align-items: center;\n"], ["\n  ", "\n\n  /* The following aligns the icon with the text, fixes bug in Firefox */\n  display: flex;\n  align-items: center;\n"])), overflowEllipsis_1.default);
var StyledIconClock = styled_1.default(icons_1.IconClock)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  /* this is solely for optics, since TimeSince always begins\n  with a number, and numbers do not have descenders */\n  margin-right: ", ";\n"], ["\n  /* this is solely for optics, since TimeSince always begins\n  with a number, and numbers do not have descenders */\n  margin-right: ", ";\n"])), space_1.default(0.5));
exports.default = Times;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=times.jsx.map