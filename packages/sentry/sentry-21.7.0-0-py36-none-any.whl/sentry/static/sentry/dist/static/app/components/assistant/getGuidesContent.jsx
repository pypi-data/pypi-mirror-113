Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
function getGuidesContent(orgSlug) {
    if (configStore_1.default.get('demoMode')) {
        return getDemoModeGuides();
    }
    return [
        {
            guide: 'issue',
            requiredTargets: ['issue_title', 'exception'],
            steps: [
                {
                    title: locale_1.t("Let's Get This Over With"),
                    target: 'issue_title',
                    description: locale_1.t("No one likes a product tour. But stick with us, and you'll find it a\n              whole lot easier to use Sentry's Issue details page."),
                },
                {
                    title: locale_1.t('Resolve Your Issues'),
                    target: 'resolve',
                    description: locale_1.t('So you fixed your problem? Congrats. Hit resolve to make it all go away.'),
                },
                {
                    title: locale_1.t('Deal With It Later, Or Never'),
                    target: 'ignore_delete_discard',
                    description: locale_1.t("Just can't deal with this Issue right now? Ignore it. Saving it for later?\n                Star it. Want it gone and out of your life forever?\n                Delete that sh*t."),
                },
                {
                    title: locale_1.t('Identify Your Issues'),
                    target: 'issue_number',
                    description: locale_1.tct("You've got a lot of Issues. That's fine. Use the Issue number in your commit message,\n                and we'll automatically resolve the Issue when your code is deployed. [link:Learn more]", { link: <externalLink_1.default href="https://docs.sentry.io/product/releases/"/> }),
                },
                {
                    title: locale_1.t('Annoy the Right People'),
                    target: 'owners',
                    description: locale_1.tct("Notification overload makes it tempting to hurl your phone into the ocean.\n                Define who is responsible for what, so alerts reach the right people and your\n                devices stay on dry land. [link:Learn more]", {
                        link: (<externalLink_1.default href="https://docs.sentry.io/product/error-monitoring/issue-owners/"/>),
                    }),
                },
                {
                    title: locale_1.t('Find Information You Can Use'),
                    target: 'tags',
                    description: locale_1.t("So many bugs, so little time. When you've got bugs as far as the mouse can scroll,\n                search and filter Events with tags or visualize Issues with a heat map."),
                },
                {
                    title: locale_1.t('Narrow Down Suspects'),
                    target: 'exception',
                    description: locale_1.t("We've got stack trace. See the exact sequence of function calls leading to the error\n                in question, no detective skills necessary."),
                },
                {
                    title: locale_1.t('Retrace Your Steps'),
                    target: 'breadcrumbs',
                    description: locale_1.t("Not sure how you got here? Sentry automatically captures breadcrumbs for events in web\n                frameworks to lead you straight to your error."),
                },
            ],
        },
        {
            guide: 'issue_stream',
            requiredTargets: ['issue_stream'],
            steps: [
                {
                    title: locale_1.t('Issues'),
                    target: 'issue_stream',
                    description: locale_1.tct("Sentry automatically groups similar events together into an issue. Similarity is\n            determined by stack trace and other factors. [link:Learn more].", {
                        link: (<externalLink_1.default href="https://docs.sentry.io/platform-redirect/?next=/data-management/event-grouping/"/>),
                    }),
                },
            ],
        },
        {
            guide: 'inbox_guide',
            requiredTargets: ['inbox_guide_tab'],
            dateThreshold: new Date(2021, 1, 26),
            steps: [
                {
                    target: 'inbox_guide_tab',
                    description: locale_1.t("We\u2019ve made some changes to help you focus on what\u2019s new."),
                    dismissText: locale_1.t("Later"),
                    nextText: locale_1.t("Take a Look"),
                    hasNextGuide: true,
                },
            ],
        },
        {
            guide: 'for_review_guide',
            requiredTargets: ['for_review_guide_tab', 'inbox_guide_reason', 'is_inbox_tab'],
            steps: [
                {
                    target: 'for_review_guide_tab',
                    description: locale_1.t("This is a list of Unresolved issues that are new or reopened in the last 7 days."),
                    cantDismiss: true,
                },
                {
                    target: 'inbox_guide_reason',
                    description: locale_1.t("These labels explain why an issue needs review."),
                    nextText: locale_1.t("When does this end?"),
                    cantDismiss: true,
                },
                {
                    target: 'inbox_guide_review',
                    description: locale_1.t("Marking an issue reviewed, resolving it, or ignoring it removes it from this list and removes the label."),
                    nextText: locale_1.t("Make It Stop Already"),
                },
            ],
        },
        {
            guide: 'assigned_or_suggested_guide',
            dateThreshold: new Date(2021, 4, 1),
            requiredTargets: ['assigned_or_suggested_query'],
            steps: [
                {
                    target: 'assigned_or_suggested_query',
                    description: locale_1.tct("Tip: use [assignedOrSuggested] to include search results based on your [ownership:ownership rules] and [committed:code you've committed].", {
                        assignedOrSuggested: <code>assigned_or_suggested</code>,
                        ownership: (<externalLink_1.default href="https://docs.sentry.io/product/error-monitoring/issue-owners/"/>),
                        committed: (<externalLink_1.default href="https://docs.sentry.io/product/sentry-basics/guides/integrate-frontend/configure-scms/"/>),
                    }),
                },
            ],
        },
        {
            guide: 'alerts_write_owner',
            requiredTargets: ['alerts_write_owner'],
            steps: [
                {
                    target: 'alerts_write_owner',
                    description: locale_1.tct("Today only admins in your organization can create alert rules but we recommend [link:allowing members to create alerts], too.", {
                        link: <link_1.default to={orgSlug ? "/settings/" + orgSlug : "/settings"}/>,
                    }),
                    nextText: locale_1.t("Allow"),
                    hasNextGuide: true,
                },
            ],
        },
        {
            guide: 'release_adoption',
            requiredTargets: ['release_adoption'],
            steps: [
                {
                    title: locale_1.t('Recalculating Adoption'),
                    target: 'release_adoption',
                    description: locale_1.t("Adoption now compares the sessions or users of a release with the total sessions or users for this project in the last 24 hours."),
                },
            ],
        },
        {
            guide: 'stack_trace_preview',
            requiredTargets: ['issue_stream_title'],
            dateThreshold: new Date(2021, 2, 15),
            steps: [
                {
                    title: locale_1.t('Stack Trace Preview'),
                    target: 'issue_stream_title',
                    description: locale_1.t("Hover over the issue title to see the stack trace of the latest event."),
                },
            ],
        },
        {
            guide: 'trace_view',
            requiredTargets: ['trace_view_guide_row', 'trace_view_guide_row_details'],
            steps: [
                {
                    title: locale_1.t('Event Breakdown'),
                    target: 'trace_view_guide_breakdown',
                    description: locale_1.t("The event breakdown shows you the breakdown of event types within a trace."),
                },
                {
                    title: locale_1.t('Transactions'),
                    target: 'trace_view_guide_row',
                    description: locale_1.t("Get an overview of every transaction. You can quickly see all the transactions in a trace alongside the project, transaction duration, and any related errors."),
                },
                {
                    title: locale_1.t('Transactions Details'),
                    target: 'trace_view_guide_row_details',
                    description: locale_1.t("Click on any transaction to see more details."),
                },
            ],
        },
        {
            guide: 'span_op_breakdowns_and_tag_explorer',
            requiredTargets: ['span_op_breakdowns_filter', 'span_op_relative_breakdowns'],
            steps: [
                {
                    title: locale_1.t('Filter by Span Operation'),
                    target: 'span_op_breakdowns_filter',
                    description: locale_1.t('You can now filter these transaction events based on http, db, browser or resource operation.'),
                },
                {
                    title: locale_1.t('Span Operation Breakdown'),
                    target: 'span_op_relative_breakdowns',
                    description: locale_1.tct('By default, you can now see how each transaction is broken down by operation. Click the spans to filter. [link:Learn more]', {
                        link: (<externalLink_1.default href="https://docs.sentry.io/product/performance/event-detail/#operations-breakdown"/>),
                    }),
                },
                {
                    title: locale_1.t('Suspect Tags'),
                    target: 'tag_explorer',
                    description: locale_1.tct("See which tags often correspond to slower transactions. You'll want to investigate these more. [link:Learn more]", {
                        link: (<externalLink_1.default href="https://docs.sentry.io/product/performance/transaction-summary/#suspect-tags"/>),
                    }),
                },
            ],
        },
        {
            guide: 'team_key_transactions',
            requiredTargets: ['team_key_transaction_header'],
            steps: [
                {
                    title: locale_1.t('Key Transactions'),
                    target: 'team_key_transaction_header',
                    description: locale_1.t('Software development is a team sport. Key Transactions allow you to mark important transactions and share them with your team.'),
                    nextText: locale_1.t('Great'),
                },
                {
                    title: locale_1.t('Migrating Key Transactions'),
                    target: 'team_key_transaction_existing',
                    description: locale_1.t('To migrate your previous key transactions, you will have to mark them as a key transaction again for your team. Sorry about that.'),
                    nextText: locale_1.t('Fine'),
                },
            ],
        },
        {
            guide: 'project_transaction_threshold',
            requiredTargets: ['project_transaction_threshold'],
            steps: [
                {
                    title: locale_1.t('Project Thresholds'),
                    target: 'project_transaction_threshold',
                    description: locale_1.t('Gauge performance using different metrics for each project. Set response time thresholds, per project, for the Apdex and User Misery Scores in each project’s Performance settings.'),
                },
            ],
        },
        {
            guide: 'project_transaction_threshold_override',
            requiredTargets: ['project_transaction_threshold_override'],
            steps: [
                {
                    title: locale_1.t('Response Time Thresholds'),
                    target: 'project_transaction_threshold_override',
                    description: locale_1.t('Use this menu to adjust each transaction’s satisfactory response time threshold, which can vary across transactions. These thresholds are used to calculate Apdex and User Misery, metrics that indicate how satisfied and miserable users are, respectively.'),
                },
            ],
        },
        {
            guide: 'percentage_based_alerts',
            requiredTargets: ['percentage_based_alerts'],
            steps: [
                {
                    title: locale_1.t('Percentage Based Alerts'),
                    target: 'percentage_based_alerts',
                    description: locale_1.tct('View the event count as a percentage of sessions and alert on this number to adapt to changes in traffic patterns. [link:View the docs] to learn more.', {
                        link: (<externalLink_1.default href="https://docs.sentry.io/product/alerts/create-alerts/issue-alert-config/#when-conditions-triggers"/>),
                    }),
                    nextText: locale_1.t('Got it'),
                },
            ],
        },
    ];
}
exports.default = getGuidesContent;
function getDemoModeGuides() {
    return [
        {
            guide: 'sidebar',
            requiredTargets: ['projects', 'issues'],
            priority: 1,
            markOthersAsSeen: true,
            steps: [
                {
                    title: locale_1.t('Projects'),
                    target: 'projects',
                    description: locale_1.t("Create a project for any type of application you want to monitor."),
                },
                {
                    title: locale_1.t('Issues'),
                    target: 'issues',
                    description: locale_1.t("Here's a list of what's broken with your application. And everything you need to know to fix it."),
                },
                {
                    title: locale_1.t('Performance'),
                    target: 'performance',
                    description: locale_1.t("See slow faster. Trace slow-loading pages back to their API calls as well as surface all related errors."),
                },
                {
                    title: locale_1.t('Releases'),
                    target: 'releases',
                    description: locale_1.t("Track the health of every release, see differences between releases from crash analytics to adoption rates."),
                },
                {
                    title: locale_1.t('Discover'),
                    target: 'discover',
                    description: locale_1.t("Query and unlock insights into the health of your entire system and get answers to critical business questions all in one place."),
                    nextText: locale_1.t("Got it"),
                },
            ],
        },
        {
            guide: 'issue_stream_v2',
            requiredTargets: ['issue_stream_title'],
            steps: [
                {
                    title: locale_1.t('Issue'),
                    target: 'issue_stream_title',
                    description: locale_1.t("Click here to get a full error report down to the line of code that caused the error."),
                },
            ],
        },
        {
            guide: 'issue_v2',
            requiredTargets: ['issue_details', 'exception'],
            steps: [
                {
                    title: locale_1.t('Details'),
                    target: 'issue_details',
                    description: locale_1.t("See the who, what, and where of every error right at the top"),
                },
                {
                    title: locale_1.t('Exception'),
                    target: 'exception',
                    description: locale_1.t("Source code right in the stack trace, so you don\u2019t need to find it yourself."),
                },
                {
                    title: locale_1.t('Tags'),
                    target: 'tags',
                    description: locale_1.t("Tags help you quickly access related events and view the tag distribution for a set of events."),
                },
                {
                    title: locale_1.t('Breadcrumbs'),
                    target: 'breadcrumbs',
                    description: locale_1.t("Check out the play by play of what your user experienced till they encountered the exception."),
                },
                {
                    title: locale_1.t('Discover'),
                    target: 'open_in_discover',
                    description: locale_1.t("Uncover trends with Discover \u2014 analyze errors by URL, geography, device, browser, etc."),
                },
            ],
        },
        {
            guide: 'releases',
            requiredTargets: ['release_version'],
            steps: [
                {
                    title: locale_1.t('Release'),
                    target: 'release_version',
                    description: locale_1.t("Click here to easily identify new issues, regressions, and track the health every release."),
                },
            ],
        },
        {
            guide: 'release_details',
            requiredTargets: ['release_chart'],
            steps: [
                {
                    title: locale_1.t('Chart'),
                    target: 'release_chart',
                    description: locale_1.t("Click and drag to zoom in on a specific section of the chart."),
                },
                {
                    title: locale_1.t('Discover'),
                    target: 'release_issues_open_in_discover',
                    description: locale_1.t("Analyze these errors by URL, geography, device, browser, etc."),
                },
                {
                    title: locale_1.t('Discover'),
                    target: 'release_transactions_open_in_discover',
                    description: locale_1.t("Analyze these performance issues by URL, geography, device, browser, etc."),
                },
            ],
        },
        {
            guide: 'discover_landing',
            requiredTargets: ['discover_landing_header'],
            steps: [
                {
                    title: locale_1.t('Discover'),
                    target: 'discover_landing_header',
                    description: locale_1.t("Click into any of the queries below to identify trends in event data."),
                },
            ],
        },
        {
            guide: 'discover_event_view',
            requiredTargets: ['create_alert_from_discover'],
            steps: [
                {
                    title: locale_1.t('Create Alert'),
                    target: 'create_alert_from_discover',
                    description: locale_1.t("Create an alert based on this query to get notified when an event exceeds user-defined thresholds."),
                },
                {
                    title: locale_1.t('Columns'),
                    target: 'columns_header_button',
                    description: locale_1.t("There's a whole lot more to... _discover_. View all the query conditions."),
                },
            ],
        },
        {
            guide: 'transaction_details',
            requiredTargets: ['span_tree'],
            steps: [
                {
                    title: locale_1.t('Span Tree'),
                    target: 'span_tree',
                    description: locale_1.t("Expand the spans to see span details from start date, end date to the operation."),
                },
                {
                    title: locale_1.t('Breadcrumbs'),
                    target: 'breadcrumbs',
                    description: locale_1.t("Check out the play by play of what your user experienced till they encountered the performance issue."),
                },
            ],
        },
    ];
}
//# sourceMappingURL=getGuidesContent.jsx.map