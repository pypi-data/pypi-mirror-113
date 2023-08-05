Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var timeSince_1 = tslib_1.__importStar(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var formatters_1 = require("app/utils/formatters");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var GroupInboxReason = {
    NEW: 0,
    UNIGNORED: 1,
    REGRESSION: 2,
    MANUAL: 3,
    REPROCESSED: 4,
};
var EVENT_ROUND_LIMIT = 1000;
function InboxReason(_a) {
    var inbox = _a.inbox, _b = _a.fontSize, fontSize = _b === void 0 ? 'sm' : _b, showDateAdded = _a.showDateAdded;
    var reason = inbox.reason, reasonDetails = inbox.reason_details, dateAdded = inbox.date_added;
    var relativeDateAdded = getDynamicText_1.default({
        value: dateAdded && timeSince_1.getRelativeDate(dateAdded, 'ago', true),
        fixed: '3s ago',
    });
    var getCountText = function (count) {
        return count > EVENT_ROUND_LIMIT
            ? "More than " + Math.round(count / EVENT_ROUND_LIMIT) + "k"
            : "" + count;
    };
    function getTooltipDescription() {
        var until = reasonDetails.until, count = reasonDetails.count, window = reasonDetails.window, userCount = reasonDetails.user_count, userWindow = reasonDetails.user_window;
        if (until) {
            // Was ignored until `until` has passed.
            // `until` format: "2021-01-20T03:59:03+00:00"
            return locale_1.tct('Was ignored until [window]', {
                window: <dateTime_1.default date={until} dateOnly/>,
            });
        }
        if (count) {
            // Was ignored until `count` events occurred
            // If `window` is defined, than `count` events occurred in `window` minutes.
            // else `count` events occurred since it was ignored.
            if (window) {
                return locale_1.tct('Occurred [count] time(s) in [duration]', {
                    count: getCountText(count),
                    duration: formatters_1.getDuration(window * 60, 0, true),
                });
            }
            return locale_1.tct('Occurred [count] time(s)', {
                count: getCountText(count),
            });
        }
        if (userCount) {
            // Was ignored until `user_count` users were affected
            // If `user_window` is defined, than `user_count` users affected in `user_window` minutes.
            // else `user_count` events occurred since it was ignored.
            if (userWindow) {
                return locale_1.tct('Affected [count] user(s) in [duration]', {
                    count: getCountText(userCount),
                    duration: formatters_1.getDuration(userWindow * 60, 0, true),
                });
            }
            return locale_1.tct('Affected [count] user(s)', {
                count: getCountText(userCount),
            });
        }
        return undefined;
    }
    function getReasonDetails() {
        switch (reason) {
            case GroupInboxReason.UNIGNORED:
                return {
                    tagType: 'default',
                    reasonBadgeText: locale_1.t('Unignored'),
                    tooltipText: dateAdded &&
                        locale_1.t('Unignored %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                    tooltipDescription: getTooltipDescription(),
                };
            case GroupInboxReason.REGRESSION:
                return {
                    tagType: 'error',
                    reasonBadgeText: locale_1.t('Regression'),
                    tooltipText: dateAdded &&
                        locale_1.t('Regressed %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                    // TODO: Add tooltip description for regression move when resolver is added to reason
                    // Resolved by {full_name} {time} ago.
                };
            // TODO: Manual moves will go away, remove this then
            case GroupInboxReason.MANUAL:
                return {
                    tagType: 'highlight',
                    reasonBadgeText: locale_1.t('Manual'),
                    tooltipText: dateAdded && locale_1.t('Moved %(relative)s', { relative: relativeDateAdded }),
                    // TODO: IF manual moves stay then add tooltip description for manual move
                    // Moved to inbox by {full_name}.
                };
            case GroupInboxReason.REPROCESSED:
                return {
                    tagType: 'info',
                    reasonBadgeText: locale_1.t('Reprocessed'),
                    tooltipText: dateAdded &&
                        locale_1.t('Reprocessed %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                };
            case GroupInboxReason.NEW:
            default:
                return {
                    tagType: 'warning',
                    reasonBadgeText: locale_1.t('New Issue'),
                    tooltipText: dateAdded &&
                        locale_1.t('Created %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                };
        }
    }
    var _c = getReasonDetails(), tooltipText = _c.tooltipText, tooltipDescription = _c.tooltipDescription, reasonBadgeText = _c.reasonBadgeText, tagType = _c.tagType;
    var tooltip = (tooltipText || tooltipDescription) && (<TooltipWrapper>
      {tooltipText && <div>{tooltipText}</div>}
      {tooltipDescription && (<TooltipDescription>{tooltipDescription}</TooltipDescription>)}
      <TooltipDescription>Mark Reviewed to remove this label</TooltipDescription>
    </TooltipWrapper>);
    return (<StyledTag type={tagType} tooltipText={tooltip} fontSize={fontSize}>
      {reasonBadgeText}
      {showDateAdded && dateAdded && (<React.Fragment>
          <Separator type={tagType !== null && tagType !== void 0 ? tagType : 'default'}>{' | '}</Separator>
          <timeSince_1.default date={dateAdded} suffix="" extraShort disabledAbsoluteTooltip/>
        </React.Fragment>)}
    </StyledTag>);
}
exports.default = InboxReason;
var TooltipWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var TooltipDescription = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var Separator = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  opacity: 80%;\n"], ["\n  color: ", ";\n  opacity: 80%;\n"])), function (p) { return p.theme.tag[p.type].iconColor; });
var StyledTag = styled_1.default(tag_1.default, {
    shouldForwardProp: function (p) { return p !== 'fontSize'; },
})(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) {
    return p.fontSize === 'sm' ? p.theme.fontSizeSmall : p.theme.fontSizeMedium;
});
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=inboxReason.jsx.map