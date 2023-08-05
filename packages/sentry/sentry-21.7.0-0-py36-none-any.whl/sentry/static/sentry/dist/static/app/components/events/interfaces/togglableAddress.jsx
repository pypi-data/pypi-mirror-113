Object.defineProperty(exports, "__esModule", { value: true });
exports.AddressToggleIcon = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("app/components/events/interfaces/utils");
var stacktracePreview_1 = require("app/components/stacktracePreview");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var TogglableAddress = function (_a) {
    var startingAddress = _a.startingAddress, address = _a.address, relativeAddressMaxlength = _a.relativeAddressMaxlength, isInlineFrame = _a.isInlineFrame, isFoundByStackScanning = _a.isFoundByStackScanning, isAbsolute = _a.isAbsolute, onToggle = _a.onToggle, isHoverPreviewed = _a.isHoverPreviewed;
    var convertAbsoluteAddressToRelative = function () {
        if (!startingAddress) {
            return '';
        }
        var relativeAddress = utils_1.formatAddress(utils_1.parseAddress(address) - utils_1.parseAddress(startingAddress), relativeAddressMaxlength);
        return "+" + relativeAddress;
    };
    var getAddressTooltip = function () {
        if (isInlineFrame && isFoundByStackScanning) {
            return locale_1.t('Inline frame, found by stack scanning');
        }
        if (isInlineFrame) {
            return locale_1.t('Inline frame');
        }
        if (isFoundByStackScanning) {
            return locale_1.t('Found by stack scanning');
        }
        return undefined;
    };
    var relativeAddress = convertAbsoluteAddressToRelative();
    var canBeConverted = !!(onToggle && relativeAddress);
    var formattedAddress = !relativeAddress || isAbsolute ? address : relativeAddress;
    var tooltipTitle = getAddressTooltip();
    var tooltipDelay = isHoverPreviewed ? stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY : undefined;
    return (<Wrapper>
      {canBeConverted && (<AddressIconTooltip title={isAbsolute ? locale_1.t('Switch to relative') : locale_1.t('Switch to absolute')} containerDisplayMode="inline-flex" delay={tooltipDelay}>
          <AddressToggleIcon onClick={onToggle} size="xs" color="purple300"/>
        </AddressIconTooltip>)}
      <tooltip_1.default title={tooltipTitle} disabled={!(isFoundByStackScanning || isInlineFrame)} delay={tooltipDelay}>
        <Address isFoundByStackScanning={isFoundByStackScanning} isInlineFrame={isInlineFrame} canBeConverted={canBeConverted}>
          {formattedAddress}
        </Address>
      </tooltip_1.default>
    </Wrapper>);
};
var AddressIconTooltip = styled_1.default(tooltip_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  align-items: center;\n  margin-right: ", ";\n"])), space_1.default(0.75));
var AddressToggleIcon = styled_1.default(icons_1.IconFilter)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"], ["\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
exports.AddressToggleIcon = AddressToggleIcon;
var getAddresstextBorderBottom = function (p) {
    if (p.isFoundByStackScanning) {
        return "1px dashed " + p.theme.red300;
    }
    if (p.isInlineFrame) {
        return "1px dashed " + p.theme.blue300;
    }
    return 'none';
};
var Address = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding-left: ", ";\n  border-bottom: ", ";\n  white-space: nowrap;\n"], ["\n  padding-left: ", ";\n  border-bottom: ", ";\n  white-space: nowrap;\n"])), function (p) { return (p.canBeConverted ? null : '18px'); }, getAddresstextBorderBottom);
var Wrapper = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  letter-spacing: -0.25px;\n  width: 100%;\n  flex-grow: 0;\n  flex-shrink: 0;\n  display: inline-flex;\n  align-items: center;\n  padding: 0 ", " 0 0;\n  order: 1;\n\n  @media (min-width: ", ") {\n    padding: 0 ", ";\n    order: 0;\n  }\n"], ["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  letter-spacing: -0.25px;\n  width: 100%;\n  flex-grow: 0;\n  flex-shrink: 0;\n  display: inline-flex;\n  align-items: center;\n  padding: 0 ", " 0 0;\n  order: 1;\n\n  @media (min-width: ", ") {\n    padding: 0 ", ";\n    order: 0;\n  }\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.textColor; }, space_1.default(0.5), function (props) { return props.theme.breakpoints[0]; }, space_1.default(0.5));
exports.default = TogglableAddress;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=togglableAddress.jsx.map