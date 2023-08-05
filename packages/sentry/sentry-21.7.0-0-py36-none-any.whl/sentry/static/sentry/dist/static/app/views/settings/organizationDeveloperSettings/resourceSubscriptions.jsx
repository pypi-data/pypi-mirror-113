Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var formContext_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formContext"));
var constants_1 = require("app/views/settings/organizationDeveloperSettings/constants");
var subscriptionBox_1 = tslib_1.__importDefault(require("app/views/settings/organizationDeveloperSettings/subscriptionBox"));
var Subscriptions = /** @class */ (function (_super) {
    tslib_1.__extends(Subscriptions, _super);
    function Subscriptions(props, context) {
        var _this = _super.call(this, props, context) || this;
        _this.onChange = function (resource, checked) {
            var events = new Set(_this.props.events);
            checked ? events.add(resource) : events.delete(resource);
            _this.save(Array.from(events));
        };
        _this.save = function (events) {
            _this.props.onChange(events);
            _this.context.form.setValue('events', events);
        };
        _this.context.form.setValue('events', _this.props.events);
        return _this;
    }
    Subscriptions.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // if webhooks are disabled, unset the events
        if (nextProps.webhookDisabled && this.props.events.length) {
            this.save([]);
        }
    };
    Subscriptions.prototype.componentDidUpdate = function () {
        var _a = this.props, permissions = _a.permissions, events = _a.events;
        var permittedEvents = events.filter(function (resource) { return permissions[constants_1.PERMISSIONS_MAP[resource]] !== 'no-access'; });
        if (JSON.stringify(events) !== JSON.stringify(permittedEvents)) {
            this.save(permittedEvents);
        }
    };
    Subscriptions.prototype.render = function () {
        var _this = this;
        var _a = this.props, permissions = _a.permissions, webhookDisabled = _a.webhookDisabled, events = _a.events;
        return (<SubscriptionGrid>
        {constants_1.EVENT_CHOICES.map(function (choice) {
                var disabledFromPermissions = permissions[constants_1.PERMISSIONS_MAP[choice]] === 'no-access';
                return (<react_1.Fragment key={choice}>
              <subscriptionBox_1.default key={choice} disabledFromPermissions={disabledFromPermissions} webhookDisabled={webhookDisabled} checked={events.includes(choice) && !disabledFromPermissions} resource={choice} onChange={_this.onChange}/>
            </react_1.Fragment>);
            })}
      </SubscriptionGrid>);
    };
    Subscriptions.defaultProps = {
        webhookDisabled: false,
    };
    Subscriptions.contextType = formContext_1.default;
    return Subscriptions;
}(react_1.Component));
exports.default = Subscriptions;
var SubscriptionGrid = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var templateObject_1;
//# sourceMappingURL=resourceSubscriptions.jsx.map